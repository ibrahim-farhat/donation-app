from django.db import models
from django.core.validators import MaxLengthValidator, MinLengthValidator, RegexValidator

from accounts.models import CustomUser
from stock.models import BloodUnit

class Donor(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    last_donation_date = models.DateField(blank=False, null=False)
    blood_type = models.PositiveSmallIntegerField(choices=BloodUnit.BloodType.choices, null=False, blank=False)
    national_id = models.CharField(
        max_length=14, unique=True, null=False, blank=False,
        validators=[
            MinLengthValidator(14),
            MaxLengthValidator(14),
            RegexValidator(r'^\d{14}$', 'National ID must be exactly 14 digits.')
        ]
    )
    
    class Meta:
        verbose_name = 'Donor'
        verbose_name_plural = 'Donors'

class Donation(models.Model):
    class VirusTestResult(models.IntegerChoices):
        POSITIVE = 1, 'Positive'
        NEGATIVE = 2, 'Negative'
        PENDING = 3, 'Pending'
    class RequestStatus(models.IntegerChoices):
        ACCEPTED = 1, 'Accepted'
        REJECTED = 2, 'Rejected'
        PENDING = 3, 'Pending'
    
    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE, 
        null=False
    )
    donation_date = models.DateTimeField(auto_now_add=True)
    number_of_units = models.PositiveIntegerField(blank=False, null=False)
    blood_virus_test = models.PositiveSmallIntegerField(choices=VirusTestResult.choices, null=False)
    status = models.PositiveSmallIntegerField(choices=RequestStatus.choices, null=False)