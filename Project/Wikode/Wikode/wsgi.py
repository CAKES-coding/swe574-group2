"""
WSGI config for Wikode project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from wikodeApp.models import RegistrationApplication, User, UserProfileInfo

if not RegistrationApplication.objects.filter(email='admin@tagpub.com').exists():
    dummy_app = RegistrationApplication(name='admin',
                                        surname='admin',
                                        email='admin@tagpub.com',
                                        applicationStatus='2',
                                        applicationText='initial admin user'
                                        )
    dummy_app.save()
    user = User.objects.create_user('admin@tagpub.com', 'admin@tagpub.com', '123456')
    user.is_superuser = True
    user.first_name = 'Admin'
    user.last_name = 'Account'
    user.save()
    user_profile = UserProfileInfo(registrationApplication=dummy_app, user=user)
    user_profile.save()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Wikode.settings')

application = get_wsgi_application()
