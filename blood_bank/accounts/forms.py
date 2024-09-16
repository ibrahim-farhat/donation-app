from django import forms

from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput
    )

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        
        return cd['password2']

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'city']