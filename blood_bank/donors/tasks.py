from django.core.mail import send_mail

from celery import shared_task
from datetime import date

from stock.models import BloodUnit
from donors.models import Donation
from blood_bank.redis import r

@shared_task
def donation_occured(new_donation_id):
    # donation.blood_virus_test = random.choice(Donation.VIRUS_TEST_CHOICES)
    donation = Donation.objects.get(id=new_donation_id)
    donation.blood_virus_test = Donation.VirusTestResult.NEGATIVE
    donor = donation.donor
    subject = (
        "Your donation process updates"
    )
    
    if donation.blood_virus_test == Donation.VirusTestResult.NEGATIVE:
        current_date = date.today()
        date_difference = current_date - donor.last_donation_date
        if date_difference.days > 90:
            donor.last_donation_date = donation.donation_date
            donation.status = Donation.RequestStatus.ACCEPTED
            donor.save()
            message = (
                "Your donation has been accepted.\n"
                "You can donate again after 3 months.\n"
                "Take care of yourself."
            )
        else:
            donation.status = Donation.RequestStatus.REJECTED
            message = (
                "Your donation has been rejected.\n"
                "We noticed that It has not been three months since your last donation.\n"
                "We are look forward to seeing you later."
            )
        
    elif donation.blood_virus_test == Donation.VirusTestResult.POSITIVE:
        donation.status = Donation.RequestStatus.REJECTED
        message = (
            "Your donation has been rejected.\n"
            "Unfortunately, your blood virus test was positive.\n"
            "We suggest that you go to the nearest hospital for follow-up and we look forward to seeing you when you are better."
        )
    donation.save()

    if donation.status == Donation.RequestStatus.ACCEPTED:
        for _ in range(donation.number_of_units):
            BloodUnit.objects.create(
                donation=donation,
                type=donation.donor.blood_type,
                deposit_date=donation.donation_date,
                availability=True,
                city=donation.donor.user.city
            )
            r.incr(f'blood_type:{donation.donor.blood_type}')

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[donor.user.email]
    )
