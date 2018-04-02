from datetime import datetime

from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from website.forms import RegisterForm, SingInForm, AddTimeForm
from website.models import UserProfile, Time


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']):
                form._errors['email'] = ['Email exist'] + form._errors.get('email', [])
                return render(request, 'website/register.html', {'form': form})
            username = form.cleaned_data['email'].split('@')[0]
            user = User(username=username)
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()
            userProfile = UserProfile(user=user, name=form.cleaned_data['name'], userType=form.cleaned_data['type'])
            userProfile.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'website/register.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SingInForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
            except Exception:
                form._errors['email'] = ['Email not exist'] + form._errors.get('email', [])
                return render(request, 'website/signin.html', {'form': form})
            if user.check_password(form.cleaned_data['password']):
                login(request, user)
                return redirect('home')
            else:
                form._errors['password'] = ['Password invalid'] + form._errors.get('password', [])
                return render(request, 'website/signin.html', {'form': form})

    else:
        form = SingInForm()
    return render(request, 'website/signin.html', {'form': form})

@login_required
def home(request):
    context = {'doctor': True}
    if request.user.profile.userType == 'doctor':
        doctor_times = Time.objects.filter(doctor=request.user.profile)
        context['doctor_times'] = doctor_times
    elif request.user.profile.userType == 'patient':
        doctor = False
        patient_times = Time.objects.filter(start__gt=datetime.now())
        patient_times = patient_times.filter(patient=request.user.profile)
        context['patient_times'] = patient_times
        context['doctor'] = False
    return render(request, 'website/home.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('login')

@login_required
def addtime(request):
    if request.method == 'POST':
        form = AddTimeForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            start_time = datetime.combine(day, form.cleaned_data['start_time'])
            end_time = datetime.combine(day, form.cleaned_data['end_time'])
            number = form.cleaned_data['number']
            delta_time = end_time - start_time
            delta_division = delta_time / number
            end_time = start_time + delta_division
            for i in range(number):
                Time.objects.create(doctor=request.user.profile, start=start_time, end=end_time)
                start_time = end_time
                end_time += delta_division
            return redirect('home')
    else:
        form = AddTimeForm()
    return render(request, 'website/addtime.html', {'form': form})

