from faker.providers import DynamicProvider

from stock.models import BloodUnit


blood_type = DynamicProvider(
    provider_name='blood_type',
    elements=BloodUnit.BloodType.values
)