from django.contrib import admin

from .models import Donor, Donation

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    exclude = []

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    exclude = []