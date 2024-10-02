from .factories import DonationFactory

from donors.services import save_donation_result
from donors.models import Donation

def test_save_donation_result_accepted(db):
    donation = DonationFactory()
    save_donation_result(donation, Donation.RequestStatus.ACCEPTED)
    assert donation.status == Donation.RequestStatus.ACCEPTED
    assert donation.donor.last_donation_date == donation.donation_date

def test_save_donation_result_rejected(db):
    donation = DonationFactory()
    save_donation_result(donation, Donation.RequestStatus.REJECTED)
    assert donation.status == Donation.RequestStatus.REJECTED
    assert donation.donor.last_donation_date != donation.donation_date