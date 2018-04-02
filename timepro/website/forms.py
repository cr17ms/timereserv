from django import forms

from website.models import UserProfile, Time

TYPE = (
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
)
class RegisterForm(forms.Form):
    email = forms.EmailField()
    name = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    type = forms.ChoiceField(choices=TYPE, required=True)


class SingInForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class TimeExplainerForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['start', 'end']


# class TimeChooserForm(ModelForm):
#     class Meta:
#         model = Time
