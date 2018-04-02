from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    TYPE = (
        ('doctor','Doctor'),
        ('patinet','Patinet'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, verbose_name='Full Name',)
    userType = models.CharField(max_length=10, choices=TYPE, default='patinet', verbose_name='User Type')

    def __str__(self):
        return self.name

class Time(models.Model):
    doctor = models.ForeignKey(UserProfile, verbose_name='Doctor', on_delete=models.CASCADE, related_name='doctor')
    start = models.DateTimeField()
    end = models.DateTimeField()
    patient = models.ForeignKey(UserProfile, null=True, verbose_name='Patient', on_delete=models.CASCADE, related_name='patient')

    def __str__(self):
        return self.doctor.name + ' @ ' + str(self.start) + ' For ' + 'No patient' if self.patient is None else self.patient.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'id':self.id })
