from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from website.forms import RegisterForm, SingInForm
from website.models import UserProfile


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
            return redirect('signin')
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
                return render(request, 'website/singin.html', {'form': form})
            if user.check_password(form.cleaned_data['password']):
                login(request, user)
                return redirect('home')
            else:
                form._errors['password'] = ['Password invalid'] + form._errors.get('password', [])
                return render(request, 'website/singin.html', {'form': form})

    else:
        form = SingInForm()
    return render(request, 'website/singin.html', {'form': form})

@login_required
def home(request):
    return HttpResponse('heeey :)')

@login_required
def signout(request):
    logout(request)
    return redirect('login')
