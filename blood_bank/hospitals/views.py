from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from accounts.models import CustomUser
from accounts.forms import UserRegistrationForm

from .forms import HospitalRegisterationForm, HospitalRequestForm
from .models import HospitalRequest, Hospital
from .tasks import process_requests

def register_hospital(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        user_specific_form = HospitalRegisterationForm(request.POST)

        if user_form.is_valid() and user_specific_form.is_valid:
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.role = CustomUser.Role.HOSPITAL
            new_user.save()
            new_donor = user_specific_form.save(commit=False)
            new_donor.user = new_user
            new_donor.save()
            messages.success(request, 'You have successfully created your account, you can login to it.')
            return redirect('dashboard')
    else:
        user_form = UserRegistrationForm()
        user_specific_form = HospitalRegisterationForm()

    return render(
        request,
        'account/register.html',
        {
            'user_form': user_form,
            'user_specific_form': user_specific_form
        }
    )

@login_required
def request(request):
    if request.user.role == CustomUser.Role.HOSPITAL:
        if request.method == 'POST':
            request_form = HospitalRequestForm(request.POST)
            if request_form.is_valid():
                new_request = request_form.save(commit=False)
                hospital = Hospital.objects.get(user=request.user)
                new_request.hospital = hospital
                new_request.request_status = HospitalRequest.RequestStatus.PENDING
                new_request.save()
                # print(r.get(f'blood_type:{BloodType.A_POS}'))
                process_requests.delay()
                messages.success(
                    request,
                    'Your request has been submitted successfully, You can check the updates through your requests list.'
                )
                return redirect('dashboard')
            else:
                messages.error(request, 'Error submitting your form.')
        else:
            request_form = HospitalRequestForm()
    else:
        messages.error(request, 'You are not authorized to go to this page.')
        return redirect('dashboard')
        
    return render(
        request,
        'request/request.html',
        {'request_form': request_form}
    )

@login_required
def request_list(request):
    if request.user.role == CustomUser.Role.HOSPITAL:
        requests = request.user.hospital.requests_created.all()
        paginator = Paginator(requests, 5)
        page = request.GET.get('page')

        try:
            requests = paginator.page(page)
        except PageNotAnInteger:
            requests = paginator.page(1)
        except EmptyPage:
            requests = paginator.page(paginator.num_pages)
        return render(
            request,
            'request/request_list.html',
            {'requests': requests}
        )
    
    else:
        messages.error(request, 'You are not authorized to go to this page.')
        return redirect('dashboard')