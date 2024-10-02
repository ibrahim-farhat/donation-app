from faker.providers import DynamicProvider

from donors.models import Donation

virus_test_result = DynamicProvider(
    provider_name='virus_test_result',
    elements=Donation.VirusTestResult.values
)

request_status = DynamicProvider(
    provider_name='request_status',
    elements=Donation.RequestStatus.values
)