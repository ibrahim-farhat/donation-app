from django.core.mail import send_mail

from celery import shared_task
from collections import defaultdict

from .models import HospitalRequest
from stock.models import BloodUnit
from blood_bank.redis import r

@shared_task
def process_requests():
    pending_requests = list(HospitalRequest.objects.filter(request_status=HospitalRequest.RequestStatus.PENDING))

    if len(pending_requests) >= 3:
        requests_by_types = defaultdict(list)
        units_per_type = defaultdict(int)

        # Devide the requests across their types, then calculate the needed number of units from every type
        for request in pending_requests:
            requests_by_types[request.blood_type].append(request)
            units_per_type[request.blood_type] = units_per_type.get(request.blood_type, 0) + request.number_of_units
        
        # Search for the types that we have enough stock of
        satisfied_types = defaultdict()
        for type in units_per_type:
            if int(r.get(f'blood_type:{type}')) >= units_per_type[type]:
                satisfied_types[type] = True
            else:
                satisfied_types[type] = False
        
        # Dict which will contain the provided units for every request
        provided_units_per_request = defaultdict(list)

        for type in satisfied_types:
            # If we have enough stock from a type, destribute it by the deposit date.
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
                requests_by_distances = defaultdict(int)
                available_units = BloodUnit.objects.filter(type=type, availability=True)

                # calculate the average distance between each hospital and all the blood units
                for request in requests_by_types[type]:
                    distances_sum = 0
                    for unit in available_units:
                        distances_sum += request.hospital.user.city.distance_to(unit.city)
                    if available_units:
                        requests_by_distances[request] = int(distances_sum / available_units.count())
                    else:
                        requests_by_distances[request] = 0


                while len(requests_by_distances):
                    available_units = BloodUnit.objects.filter(type=type, availability=True)
                    available_units_count = int(r.get(f'blood_type:{type}') or 0)
                    
                    # List to store requests to remove after the loop
                    requests_to_remove = []

                    # filter the unsatisfied requests
                    for request in requests_by_distances:
                        if available_units_count < request.number_of_units:
                            request.request_status = HospitalRequest.RequestStatus.REJECTED
                            request.save()
                            requests_to_remove.append(request)
                    
                    for request in requests_to_remove:
                        requests_by_distances.pop(request)

                    # break if there is not any requests
                    if not len(requests_by_distances):
                        break
                    
                    # calculate the least distance
                    least_distance = min(requests_by_distances.values())
                    
                    # search if there are any duplicates with the same distance
                    similar_requests_in_distance = [req for req, dist in requests_by_distances.items() if dist == least_distance]
                    
                    # handle the case if there is only one request with the least distance
                    if len(similar_requests_in_distance) == 1:
                        request = similar_requests_in_distance[0]
                        # mark the request as accepted
                        request.request_status = HospitalRequest.RequestStatus.ACCEPTED
                        request.save()
                        # provide the request with its units
                        available_units = sorted(available_units, key=lambda unit: request.hospital.user.city.distance_to(unit.city))
                        provided_units_per_request[request] = available_units[:request.number_of_units]
                        # update the database by withdrawing these units
                        r.decrby(f'blood_type:{type}', request.number_of_units)
                        for unit in provided_units_per_request[request]:
                            unit.availability = False
                            unit.save()
                        requests_by_distances.pop(request)

                    else:
                        # search for the worst patient status among those requests
                        worst_patient_status = HospitalRequest.PatientStatus.NORMAL
                        request_to_service = HospitalRequest()
                        for request in similar_requests_in_distance:
                            if request.patient_status <= worst_patient_status:
                                worst_patient_status = request.patient_status
                                request_to_service = request
                        
                        request = request_to_service
                        # mark the request as accepted
                        request.request_status = HospitalRequest.RequestStatus.ACCEPTED
                        request.save()
                        # provide the request with its units
                        sorted(available_units, key=lambda unit: request.hospital.user.city.distance_to(unit.city))
                        provided_units_per_request[request] = available_units[:request.number_of_units]
                        # update the database by withdrawing these units
                        r.decrby(f'blood_type:{type}', request.number_of_units)
                        for unit in provided_units_per_request[request]:
                            unit.availability = False
                            unit.save()
                        requests_by_distances.pop(request)


        for request in pending_requests:
            subject = (
                "Your request process updates"
            )
            message = (
                "Your have recieved new updates about your early request.\n\n"
                "Please, go to your portal so you can see what is going on."
            )

            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[request.hospital.user.email]
            )
        print(provided_units_per_request)