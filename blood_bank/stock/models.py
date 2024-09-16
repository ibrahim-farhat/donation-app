from django.db import models

from city.models import City


class BloodUnit(models.Model):
    class BloodType(models.IntegerChoices):
        A_POS = 1, 'A+'
        A_NEG = 2, 'A-'
        B_POS = 3, 'B+'
        B_NEG = 4, 'B-'
        O_POS = 5, 'O+'
        O_NEG = 6, 'O-'
        AB_POS = 7, 'AB+'
        AB_NEG = 8, 'AB-'

    donation = models.ForeignKey(
        'donors.Donation',
        on_delete=models.SET_NULL,
        null=True
    )
    type = models.PositiveSmallIntegerField(choices=BloodType.choices, null=False, blank=False)
    deposit_date = models.DateTimeField()
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False)
    availability = models.BooleanField(null=False, blank=False)
