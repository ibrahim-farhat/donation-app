from django.contrib import admin

from .models import Hospital, HospitalRequest

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    exclude = []

@admin.register(HospitalRequest)
class HospitalRequestAdmin(admin.ModelAdmin):
    list_display = ['hospital', 'number_of_units', 'blood_type', 'request_status']
    exclude = []