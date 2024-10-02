from django.template.loader import render_to_string
from django.core.mail import send_mail

from collections import defaultdict

# from blood_bank.redis import r
from stock.models import BloodUnit
from stock.selectors import fetch_available_blood_units_by_type, fetch_available_blood_units_ordered_by_city
from .models import HospitalRequest

DEFAULT_REDIS_COUNT = 0

    
def classify_requests_by_types(hospital_requests: list[HospitalRequest]) -> dict[BloodUnit.BloodType, list[HospitalRequest]]:
    """Classify requests by blood type."""

    requests_by_types = defaultdict(list)

    for request in hospital_requests:
        requests_by_types[request.blood_type].append(request)

    return requests_by_types

def calculate_requests_needed_units(hospital_requests: list[HospitalRequest]) -> dict[BloodUnit.BloodType, int]:
    """Calculate needed units for each type."""

    units_per_type = defaultdict(int)

    for request in hospital_requests:
        units_per_type[request.blood_type] += request.number_of_units
    
    return units_per_type


def check_stock_availability(units_per_type: dict[BloodUnit.BloodType]):
    """Check if there is enough stock for each blood type."""

    classified_types = {}

    for blood_type, units_needed in units_per_type.items():
        # available_units = int(r.get(f'blood_type:{blood_type}') or DEFAULT_REDIS_COUNT)
        available_units = len(fetch_available_blood_units_by_type(blood_type))
        classified_types[blood_type] = available_units >= units_needed

    return classified_types

def update_database_with_accepted_request(request: HospitalRequest, provided_units: list[BloodUnit]):
    """Free blood units from database and update request status."""

    # Update Redis and database
    # r.decrby(f'blood_type:{request.blood_type}', request.number_of_units)
    BloodUnit.objects.filter(id__in=[unit.id for unit in provided_units]).update(availability=False)

    # Mark the request as accepted
    request.request_status = HospitalRequest.RequestStatus.ACCEPTED
    request.save()

def update_database_with_rejected_request(request: HospitalRequest):
    # Mark the request as rejected
    request.request_status = HospitalRequest.RequestStatus.REJECTED
    request.save()

def calculate_requests_with_distances(requests: HospitalRequest, available_units: list[BloodUnit]) -> dict[HospitalRequest]:
    """Calculate distances between requests' city and available units' cities."""
    
    requests_with_distances = {}
    
    for request in requests:
        total_distance = sum(request.hospital.user.city.distance_to(unit.city) for unit in available_units)
        avg_distance = total_distance / len(available_units)
        requests_with_distances[request] = avg_distance
    
    return requests_with_distances

def get_least_distance_among_requests(requests_with_distances: dict[HospitalRequest]) -> float:
    """Calculate the least distance."""

    return min(requests_with_distances.values())

def get_similar_requests(requests_with_distances: dict[HospitalRequest], distance: float) -> list[HospitalRequest]:
    """Get similar requests in distance between its city and available units city."""

    # search if there are any duplicates with the same distance
    similar_requests_in_distance = [req for req, dist in requests_with_distances.items() if dist == distance]

    return similar_requests_in_distance

def handle_satisfied_type_requests(blood_type: BloodUnit.BloodType, requests: list[HospitalRequest], provided_units_per_request: dict[HospitalRequest]) -> None:
    """Handle requests for which there is enough stock of the required blood type."""


    for request in requests:
        available_units = fetch_available_blood_units_by_type(blood_type)
        provided_units_per_request[request] = available_units[:request.number_of_units]
        update_database_with_accepted_request(request, provided_units_per_request[request])

    print(provided_units_per_request)

def reject_unsatisfied_requests(blood_type: BloodUnit.BloodType, requests: list[HospitalRequest], requests_with_distances:dict[HospitalRequest, float]=None) -> None:
    """Reject and remove requests that we have not enough stock for."""

    available_units = fetch_available_blood_units_by_type(blood_type)

    # List to store requests to remove after the loop
    requests_to_remove = []

    # filter unsatisfied requests
    for request in requests:
        if len(available_units) < request.number_of_units:
            update_database_with_rejected_request(request)
            requests_to_remove.append(request)

    if requests_with_distances:
        for request in requests_to_remove:
            requests_with_distances.pop(request)

def get_worst_request(requests: HospitalRequest) -> HospitalRequest:
    """Get the worst request by the patient status among requests."""

    worst_patient_status = HospitalRequest.PatientStatus.NORMAL
    worst_request = HospitalRequest()
    
    for request in requests:
        if request.patient_status <= worst_patient_status:
            worst_patient_status = request.patient_status
            worst_request = request

    return worst_request

def handle_unsatisfied_type_requests(blood_type: BloodUnit.BloodType, requests: list[HospitalRequest], provided_units_per_request: dict[HospitalRequest]) -> None:
    """Handle requests for which there is not enough stock."""
    
    # Calculate the distances between every request and available blood units
    available_units = fetch_available_blood_units_by_type(blood_type)

    requests_with_distances = dict()
    if available_units:
        requests_with_distances = calculate_requests_with_distances(requests, available_units)
    else:
        reject_unsatisfied_requests(blood_type, requests)

    while requests_with_distances:
        reject_unsatisfied_requests(blood_type, requests_with_distances.keys(), requests_with_distances)

        # break if there is no longer any requests
        if not len(requests_with_distances):
            break

        least_distance = get_least_distance_among_requests(requests_with_distances)
        similar_requests = get_similar_requests(requests_with_distances, least_distance)

        if(len(similar_requests) == 1):
            request_to_service = similar_requests[0] 
        else:
            # search for the worst patient status among those requests
            request_to_service = get_worst_request(similar_requests)

        # provide the request with its units
        available_units = fetch_available_blood_units_ordered_by_city(blood_type, request_to_service.hospital.user.city)
        provided_units_per_request[request_to_service] = available_units[:request_to_service.number_of_units]
        
        update_database_with_accepted_request(request_to_service, provided_units_per_request[request_to_service])
        requests_with_distances.pop(request_to_service)

def send_notification_email(request):
    """Send an email notification to the hospital about the request update."""

    subject = "Update on Your Blood Request"
    message = render_to_string('request/request_update_email.html', {'request': request})

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@bloodbank.com',
            recipient_list=[request.hospital.user.email],
            fail_silently=False
        )

    except Exception as e:
        print(f"Error sending email for request {request.id}: {str(e)}")
