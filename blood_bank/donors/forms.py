from django import forms

from .models import Donor, Donation
    
class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['national_id', 'first_name', 'last_name', 'date_of_birth', 'last_donation_date', 'blood_type']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['number_of_units']
