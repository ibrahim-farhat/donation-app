from stock.services import create_bulk_of_blood_units

from .models import Donation

def save_donation_result(donation: Donation, result: Donation.RequestStatus) -> None:
    
    if result == Donation.RequestStatus.ACCEPTED:
          create_bulk_of_blood_units(donation)
          donation.donor.last_donation_date = donation.donation_date
          donation.donor.save()
    
    donation.status = result
    donation.save()