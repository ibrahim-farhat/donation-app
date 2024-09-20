from django.utils import timezone

from celery import shared_task
from datetime import timedelta

from .models import BloodUnit

"""
The command that used to create the periodic task of the expired blood units filteration.
"""
# from django_celery_beat.models import PeriodicTask, CrontabSchedule

# # Create a crontab schedule for midnight every day
# schedule, created = CrontabSchedule.objects.get_or_create(minute='0', hour='0')

# # Create the periodic task
# task = PeriodicTask.objects.create(
#     crontab=schedule,
#     name='Expired Blood Units Filteration', 
#     task='stock.tasks.filter_expired_blood_units', 
# )

@shared_task
def filter_expired_blood_units():
    three_months_ago_datetime = timezone.now() - timedelta(days=90)
    expired_units = BloodUnit.objects.filter(deposit_date__lt=three_months_ago_datetime, availability=True)
    for unit in expired_units:
        unit.availability = False
        unit.save()