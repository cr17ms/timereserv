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


class TimeExplainerForm(forms.ModelForm):
    class Meta:
        model = Time
        fields = ['start', 'end']


# class TimeChooserForm(ModelForm):
#     class Meta:
#         model = Time
