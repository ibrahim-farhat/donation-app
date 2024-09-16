from django.db import models

from accounts.models import CustomUser
from stock.models import BloodUnit

class Hospital(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='hospital'
    )
    hospital_name = models.CharField(max_length=150, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'

class HospitalRequest(models.Model):
    class PatientStatus(models.IntegerChoices):
        IMMEDIATE = 1, 'Immediate'
        URGENT = 2, 'Urgent'
        NORMAL = 3, 'Normal'
    class RequestStatus(models.IntegerChoices):
        ACCEPTED = 1, 'Accepted'
        REJECTED = 2, 'Rejected'
        PENDING = 3, 'Pending'

    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name='requests_created',
    )
    request_date = models.DateTimeField(auto_now_add=True)
    number_of_units = models.PositiveIntegerField(blank=False, null=False)
    blood_type = models.PositiveSmallIntegerField(choices=BloodUnit.BloodType.choices, blank=False, null=False)
    patient_status = models.PositiveSmallIntegerField(choices=PatientStatus.choices, blank=False, null=False)
    request_status = models.PositiveSmallIntegerField(choices=RequestStatus.choices, blank=False, null=False)
    
    class Meta:
        ordering = ['-request_date']
