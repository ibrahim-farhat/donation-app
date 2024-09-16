from django.core.mail import send_mail

from celery import shared_task
from collections import defaultdict

from .models import HospitalRequest
from stock.models import BloodUnit
from blood_bank.redis import r

@shared_task
def process_requests():
    pending_requests = list(HospitalRequest.objects.filter(request_status=HospitalRequest.RequestStatus.PENDING))

    if len(pending_requests) >= 10:
        requests_by_types = defaultdict(list)
        units_per_type = defaultdict(int)

        for request in pending_requests:
            requests_by_types[request.blood_type].append(request)
            units_per_type[request.blood_type] = units_per_type.get(request.blood_type, 0) + request.number_of_units

        
        satisfied_types = defaultdict()

        for type in units_per_type:
            if int(r.get(f'blood_type:{type}') or 0) >= units_per_type[type]:
                satisfied_types[type] = True
            else:
                satisfied_types[type] = False
        
        provided_units_per_request = defaultdict(list)

        for type in satisfied_types:
            if satisfied_types[type]:
                for request in requests_by_types[type]:
                    # mark the request as accepted
                    request.request_status = HospitalRequest.RequestStatus.ACCEPTED
                    request.save()
                    # provide the request with its units
                    provided_units_per_request[request] = BloodUnit.objects.filter(type=type, availability=True).order_by('deposit_date')[:request.number_of_units]
                    # update the database by withdrawing these units
                    r.decrby(f'blood_type:{type}', request.number_of_units)
                    for unit in provided_units_per_request[request]:
                        unit.availability = False
                        unit.save()
            elif not satisfied_types[type]:
                available_units = BloodUnit.objects.filter(type=type, availability=True).order_by('deposit_date')
                requests_by_distances = defaultdict(list)

                for request in requests_by_types[type]:
                    for unit in available_units:
                        requests_by_distances[request].append((unit, request.hospital.user.city.distance_to(unit.city), request.patient_status))
                    # sort every list of tuples by the distance between the hospital and the blood unit.
                    requests_by_distances[request].sort(key=lambda x: x[1])

                while len(requests_by_distances):
                    available_units_count = r.get(f'blood_type:{type}')
                    least_distance = 99999999999
                    for request in requests_by_distances:
                        if available_units_count < request.number_of_units:
                            request.request_status = HospitalRequest.RequestStatus.REJECTED
                            request.save()
                            requests_by_distances.pop(request)
                        else:
                            for tuple in requests_by_distances[request]:
                                if tuple[1] < least_distance:
                                    least_distance = tuple[1]
                    
                    similar_requests_in_distance = list()
                    for request in requests_by_distances:
                        tuple = requests_by_distances[request][0]
                        if tuple[1] == least_distance:
                            similar_requests_in_distance.append((request, tuple[0], tuple[1], tuple[2]))

                    worst_patient_status = HospitalRequest.PatientStatus
                    request_to_service = HospitalRequest()
                    for tuple in similar_requests_in_distance:
                        if tuple[3] <= worst_patient_status:
                            worst_patient_status = tuple[3]
                            request_to_service = tuple[0]

                    # mark the request as accepted
                    request_to_service.request_status = HospitalRequest.RequestStatus.ACCEPTED
                    request_to_service.save()
                    for _ in range(request_to_service.number_of_units):
                        provided_units_per_request[request_to_service].append(requests_by_distances[request][_])
                        
                        # remove any occurence of the unit that has been used
                        for request in requests_by_distances:
                            for tuple in requests_by_distances[request]:
                                if tuple[0] == requests_by_distances[request_to_service][0][0]:
                                    requests_by_distances[request].remove(tuple)

                        # remove the request itself from the requests_by_distances dict
                        requests_by_distances.pop(request)

                    # update the database by withdrawing these units
                    r.decrby(f'blood_type:{type}', request.number_of_units)
                    for unit in provided_units_per_request[request_to_service]:
                        unit.availability = False
                        unit.save()


        
        # print(requests_by_distances)
            
        
        # accepted_requests = pending_requests

        # for request in accepted_requests:
        #     request.request_status = HospitalRequest.RequestStatus.ACCEPTED
        #     request.save()
        #     subject = (
        #         "Your request process updates"
        #     )
        #     message = (
        #         "Your have recieved new updates about your early request.\n\n"
        #         "Please, go to your portal so you can see what is going on."
        #     )

        #     send_mail(
        #         subject=subject,
        #         message=message,
        #         from_email=None,
        #         recipient_list=[request.hospital.user.email]
        #     )
        # for request in accepted_requests:
        #     units_to_withdrawn = BloodUnit.objects.filter(type = request.blood_type).order_by('deposit_date')[:request.number_of_units]
        #     for unit in units_to_withdrawn:
        #         unit.delete()
