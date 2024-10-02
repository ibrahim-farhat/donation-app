import pytest

from donors.tests.factories import DonationFactory
from donors.selectors import get_donation_by_id
from donors.models import Donation

def test_get_donation_by_id(db):
    DonationFactory(id=10)
    donation = get_donation_by_id(10)
    assert donation.id == 10

def test_get_donation_by_id_not_exist(db):
    with pytest.raises(Donation.DoesNotExist):
        get_donation_by_id(10)
    