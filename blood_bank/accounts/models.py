from django.contrib.auth.models import AbstractUser
from django.db import models

from city.models import City

class CustomUser(AbstractUser):
    class Role(models.IntegerChoices):
        DONOR = 1, 'Donor'
        HOSPITAL = 2, 'Hospital'

    first_name = None
    last_name = None
    email = models.EmailField(unique=True, null=False, blank=False)
    role = models.PositiveSmallIntegerField(choices=Role.choices, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'