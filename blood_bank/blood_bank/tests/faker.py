from faker import Faker

from donors.tests.providers import virus_test_result, request_status
from accounts.tests.providers import role
from stock.tests.providers import blood_type

faker = Faker()

faker.add_provider(role)
faker.add_provider(blood_type)
faker.add_provider(virus_test_result)
faker.add_provider(request_status)