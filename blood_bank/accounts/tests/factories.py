from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from blood_bank.tests.faker import faker
from city.tests.factories import CityFactory
from accounts.models import CustomUser

class UserFactory(DjangoModelFactory):
    city = SubFactory(CityFactory)
    username = LazyAttribute(lambda _: faker.user_name())
    email = LazyAttribute(lambda _: faker.email())
    role = LazyAttribute(lambda _: faker.role())

    class Meta:
        model = 'accounts.CustomUser'