from django.contrib import admin
from .models import RegistrationApplication, UserProfileInfo


admin.site.register(UserProfileInfo)
admin.site.register(RegistrationApplication)
