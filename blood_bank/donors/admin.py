from django.contrib import admin

from .models import Donor, Donation

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_type', 'last_donation_date']

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'number_of_units', 'status']