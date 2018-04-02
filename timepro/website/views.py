from django.shortcuts import render
from django.contrib.auth.models import User

from website.forms import RegisterForm
from website.models import UserProfile


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']):
                form._errors['email'] = ['Email exist'] + form._errors.get('email', [])
                return render(request, 'website/home.html', {'form': form})
            username = form.cleaned_data['email'].split('@')[0]
            user = User(username=username)
            user.set_password(form.cleaned_data['password'])
            user.email = form.cleaned_data['email']
            user.save()
            userProfile = UserProfile(user=user, name=form.cleaned_data['name'], userType=form.cleaned_data['type'])
            userProfile.save()
    else:
        form = RegisterForm()
    return render(request, 'website/home.html', {'form': form})
