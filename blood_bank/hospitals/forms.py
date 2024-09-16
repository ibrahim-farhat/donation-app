from django import forms

from .models import Hospital, HospitalRequest

class HospitalRegisterationForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['hospital_name']

class HospitalRequestForm(forms.ModelForm):
    class Meta:
        model = HospitalRequest
        fields = ['number_of_units', 'blood_type', 'patient_status']