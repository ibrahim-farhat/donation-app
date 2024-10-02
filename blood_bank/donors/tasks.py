from celery import shared_task

from donors.models import Donation

from .selectors import get_donation_by_id
from .services import save_donation_result
from .helpers import calculate_days_from_last_donation, DonationEmailCode, send_response_email

@shared_task
def donation_occured(new_donation_id):
    new_donation = get_donation_by_id(new_donation_id)
    new_donation.blood_virus_test = Donation.VirusTestResult.NEGATIVE
    # new_donation.blood_virus_test = random.choice(Donation.VIRUS_TEST_CHOICES)
    donor = new_donation.donor
    
    if new_donation.blood_virus_test == Donation.VirusTestResult.NEGATIVE:
        
        days_from_last_donation = calculate_days_from_last_donation(donor)
        
        if days_from_last_donation <= 90:
            request_status = Donation.RequestStatus.REJECTED
            email_code = DonationEmailCode.REJECTED_NOT_ENOUGH_TIME

        else:
            request_status = Donation.RequestStatus.ACCEPTED
            email_code = DonationEmailCode.ACCEPTED

    elif new_donation.blood_virus_test == Donation.VirusTestResult.POSITIVE:
        request_status = Donation.RequestStatus.REJECTED
        email_code = DonationEmailCode.REJECTED_POS_VIRUS_TEST
    
    save_donation_result(new_donation, request_status)
    send_response_email(new_donation, email_code)