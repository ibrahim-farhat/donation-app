from django.db import models
from django.core.mail import send_mail

from datetime import date

from .models import Donation, Donor

class DonationEmailCode(models.IntegerChoices):
    ACCEPTED = 1
    REJECTED_NOT_ENOUGH_TIME = 2
    REJECTED_POS_VIRUS_TEST = 3
    
def send_response_email(donation: Donation, donation_email_code: DonationEmailCode) -> None:
    """Send an email notification to the donor about the donation result."""

    subject = (
        "Your donation process updates"
    )

    if donation_email_code == DonationEmailCode.ACCEPTED:
        message = (
            "Your donation has been accepted.\n"
            "You can donate again after 3 months.\n"
            "Take care of yourself."
        )
    elif donation_email_code == DonationEmailCode.REJECTED_NOT_ENOUGH_TIME:
        message = (
            "Your donation has been rejected.\n"
            "We noticed that It has not been three months since your last donation.\n"
            "We are look forward to seeing you later."
        )
    elif donation_email_code == DonationEmailCode.REJECTED_POS_VIRUS_TEST:
        message = (
            "Your donation has been rejected.\n"
            "Unfortunately, your blood virus test was positive.\n"
            "We suggest that you go to the nearest hospital for follow-up and we look forward to seeing you when you are better."
        )
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='noreply@bloodbank.com',
            recipient_list=[donation.donor.user.email],
            fail_silently=False
        )
    except Exception as e:
        print(f"Error sending email for donation {donation.id}: {str(e)}")

def calculate_days_from_last_donation(donor: Donor) -> int:
    """Calculate the number of days since the donor's last donation."""
    
    current_date = date.today()
    date_difference = current_date - donor.last_donation_date
    
    return date_difference.days