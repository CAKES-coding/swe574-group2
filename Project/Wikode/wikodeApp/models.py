from django.db import models


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
