from django.contrib import admin
from .models import RegistrationApplication, UserProfileInfo, FollowRelation


admin.site.register(UserProfileInfo)
admin.site.register(RegistrationApplication)
admin.site.register(FollowRelation)
