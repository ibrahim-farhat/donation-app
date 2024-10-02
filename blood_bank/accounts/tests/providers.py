from faker.providers import DynamicProvider

from accounts.models import CustomUser

role = DynamicProvider(
    provider_name='role',
    elements=CustomUser.Role.values
)
