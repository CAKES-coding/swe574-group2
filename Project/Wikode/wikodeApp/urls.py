from django.urls import path
from wikodeApp import views

app_name = 'wikodeApp'

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('registration/', views.registration, name='registration'),
    path('registrationRequests/', views.registrationRequests, name='registrationRequests'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userList/', views.userList, name='userList'),
    path('articleDetail/<int:pk>', views.articleDetail, name='articleDetail'),
]