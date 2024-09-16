from django.contrib import admin

from .models import BloodUnit

@admin.register(BloodUnit)
class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'city', 'availability']
    exclude = []