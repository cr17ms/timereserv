from django import forms
from django.contrib.admin import widgets

from website.models import UserProfile, Time

TYPE = (
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
)
class RegisterForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    type = forms.ChoiceField(choices=TYPE, required=True, initial='patient')


class SingInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class AddTimeForm(forms.Form):
    day = forms.DateField(widget=widgets.AdminDateWidget())
    start_time = forms.TimeField(widget=widgets.AdminTimeWidget())
    end_time = forms.TimeField(widget=widgets.AdminTimeWidget())
    number = forms.IntegerField(max_value=10, min_value=1, initial=1)
