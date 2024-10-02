from factory import LazyAttribute
from factory.django import DjangoModelFactory

from blood_bank.tests.faker import faker
from city.models import City

class CityFactory(DjangoModelFactory):
    name = LazyAttribute(lambda _: faker.city())
    latitude = LazyAttribute(lambda _: faker.latitude())
    longitude = LazyAttribute(lambda _: faker.longitude())

    class Meta:
        model = City