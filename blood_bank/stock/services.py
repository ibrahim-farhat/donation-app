from .models import BloodUnit
from donors.models import Donation
# from blood_bank.redis import r

def create_bulk_of_blood_units(donation: Donation) -> None:
    blood_units = []

    for _ in range(donation.number_of_units):
        blood_units.append(
            BloodUnit(
                donation=donation,
                type=donation.donor.blood_type,
                deposit_date=donation.donation_date,
                availability=True,
                city=donation.donor.user.city
            )
        )
    
    BloodUnit.objects.bulk_create(blood_units)
    
    # r.incrby(f'blood_type:{donation.donor.blood_type}', donation.number_of_units)
