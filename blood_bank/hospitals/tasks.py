from django.core.mail import send_mail

from celery import shared_task
from collections import defaultdict

from .models import HospitalRequest
from stock.models import BloodUnit
from blood_bank.redis import r

from .selectors import fetch_pending_requests
from .helpers import send_notification_email, check_stock_availability, classify_requests_by_types, calculate_requests_needed_units, handle_satisfied_type_requests, handle_unsatisfied_type_requests

NUMBER_OF_REQUESTS_PER_CYCLE = 10

@shared_task
def process_requests():
    pending_requests = fetch_pending_requests()

    if pending_requests.count() < NUMBER_OF_REQUESTS_PER_CYCLE:
        print('Not enough pending requests to process.')
        return

    requests_classified_by_types = classify_requests_by_types(pending_requests)
    needed_units_per_type = calculate_requests_needed_units(pending_requests)
    satisfied_types = check_stock_availability(needed_units_per_type)
    provided_units_per_request = defaultdict(list[BloodUnit])

    for blood_type, is_satisfied in satisfied_types.items():
        if is_satisfied:
            handle_satisfied_type_requests(blood_type, requests_classified_by_types[blood_type], provided_units_per_request)
        else:
            handle_unsatisfied_type_requests(blood_type, requests_classified_by_types[blood_type], provided_units_per_request)
    for request in pending_requests:
        send_notification_email(request)
    
    print(f'Provided units: {provided_units_per_request}')