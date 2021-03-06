"""Wikode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from wikodeApp.views import homePage, userLogout, TagAutocomplete
from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path('', homePage, name='home'),
    path('wikode/', include('wikodeApp.urls')),
    path('admin/', admin.site.urls),
    path('logout/', userLogout, name='logout'),
    path('tag-autocomplete/', TagAutocomplete.as_view(), name='tag-autocomplete'),
]

handler404 = 'wikodeApp.views.error'
handler500 = 'wikodeApp.views.error'
handler403 = 'wikodeApp.views.error'
handler400 = 'wikodeApp.views.error'