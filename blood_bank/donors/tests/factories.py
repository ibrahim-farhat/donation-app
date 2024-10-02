from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from blood_bank.tests.faker import faker
from accounts.tests.factories import UserFactory
from donors.models import Donation, Donor

from .helpers import generate_national_id

class DonorFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    first_name = LazyAttribute(lambda _: faker.name())
    last_name = LazyAttribute(lambda _: faker.name())
    date_of_birth = LazyAttribute(lambda _: faker.date_of_birth())
    last_donation_date = LazyAttribute(lambda _: faker.date())
    blood_type = LazyAttribute(lambda _: faker.blood_type())
    national_id = LazyAttribute(lambda _: generate_national_id())

    class Meta:
        model = 'donors.Donor'

class DonationFactory(DjangoModelFactory):
    donor = SubFactory(DonorFactory)
    donation_date = LazyAttribute(lambda _: faker.date())
    number_of_units = LazyAttribute(lambda _: faker.random_int())
    blood_virus_test = LazyAttribute(lambda _: faker.virus_test_result())
    status = LazyAttribute(lambda _: Donation.RequestStatus.PENDING)

    class Meta:
        model = 'donors.Donation'