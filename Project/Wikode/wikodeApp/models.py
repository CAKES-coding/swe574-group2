from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class RegistrationApplication(models.Model):
    applicationStatuses = (
        ('1', 'New'),
        ('2', 'Approved'),
        ('3', 'Rejected')
    )

    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    email = models.EmailField()
    applicationText = models.TextField(max_length=512)
    applicationDate = models.DateTimeField(default=timezone.now)
    applicationStatus = models.CharField(max_length=20, choices=applicationStatuses, default='1')


class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registrationApplication = models.ForeignKey(RegistrationApplication, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
