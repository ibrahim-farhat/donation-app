from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from accounts.forms import UserRegistrationForm

from .models import Donation, Donor
from .forms import DonorRegistrationForm, DonationForm
from .tasks import donation_occured

def register_donor(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        user_specific_form = DonorRegistrationForm(request.POST)

        if user_form.is_valid() and user_specific_form.is_valid:
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.role = CustomUser.Role.DONOR
            new_user.save()
            new_donor = user_specific_form.save(commit=False)
            new_donor.user = new_user
            new_donor.save()
            messages.success(request, 'You have successfully created your account, you can login to it.')
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        user_specific_form = DonorRegistrationForm()

    return render(
        request,
        'account/register.html',
        {
            'user_form': user_form,
            'user_specific_form': user_specific_form
        }
    )

@login_required
def donate(request):
    if request.user.role == CustomUser.Role.DONOR:
        if request.method == 'POST':
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                new_donation = donation_form.save(commit=False)
                donor = Donor.objects.get(user=request.user)
                new_donation.donor = donor
                new_donation.blood_virus_test = Donation.VirusTestResult.PENDING
                new_donation.status = Donation.RequestStatus.PENDING
                new_donation.save()
                donation_occured.delay(new_donation.id)
                messages.success(
                    request,
                    'Your donation has been submitted successfully, You will be informed by mail for the updates.'
                )
                return redirect('dashboard')
            else:
                messages.error(request, 'Error submitting your form.')
            
        else:
            donation_form = DonationForm()
    else:
        messages.error(request, 'You are not authorized to go to donation page.')
        return redirect('dashboard')

    return render(
        request,
        'donation/donate.html',
        {'donation_form': donation_form}
    )
