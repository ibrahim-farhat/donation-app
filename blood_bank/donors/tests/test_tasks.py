from datetime import date

from donors.tasks import donation_occured
from donors.models import Donation

from .factories import DonationFactory

def test_donation_occured_accepted(db):
    donation = DonationFactory(status=Donation.RequestStatus.PENDING, donor__last_donation_date=date.today(), blood_virus_test=Donation.VirusTestResult.NEGATIVE)
    # donation.donor.last_donation_date = date.today()
    # donation.blood_virus_test = Donation.VirusTestResult.NEGATIVE

    donation_occured(donation.id)


    assert donation.status == Donation.RequestStatus.REJECTED