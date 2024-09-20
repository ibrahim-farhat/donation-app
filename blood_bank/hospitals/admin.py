from django.contrib import admin

from .models import Hospital, HospitalRequest

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ['user', 'hospital_name']

@admin.register(HospitalRequest)
class HospitalRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'number_of_units', 'patient_status', 'blood_type', 'request_status']