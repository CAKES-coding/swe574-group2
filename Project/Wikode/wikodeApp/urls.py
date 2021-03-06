from django.urls import path
from wikodeApp import views

app_name = 'wikodeApp'

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('registration/', views.registration, name='registration'),
    path('registrationRequests/', views.registrationRequests, name='registrationRequests'),
    path('userLogin/', views.userLogin, name='userLogin'),
    path('profile/', views.myProfilePage, name='myProfilePage'),
    path('profile/<int:pk>', views.getProfilePageOfOtherUser, name='getProfilePageOfOtherUser'),
    path('userList/', views.userList, name='userList'),
    path('getArticles/', views.getArticles, name='getArticles'),
    path('articleDetail/<int:pk>', views.articleDetail, name='articleDetail'),
    path('profile/<int:pk>/follow', views.followUser, name='followUser'),
    path('vote/', views.vote, name='vote'),
]
