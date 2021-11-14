from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from wikodeApp.forms import ApplicationRegistrationForm, GetArticleForm
from wikodeApp.models import RegistrationApplication, Article
from wikodeApp.utils.fetchArticles import createArticles
import string
import random


@login_required
def homePage(request):
    return render(request, 'wikodeApp/homePage.html')


def registration(request):
    if request.method == 'POST':
        registration_form = ApplicationRegistrationForm(data=request.POST)
        if registration_form.is_valid():
            if RegistrationApplication.objects.filter(email=request.POST['email']).filter(
                    applicationStatus='1').exists():
                return render(request, 'wikodeApp/registration.html', {'form': registration_form,
                                                                       'under_review': 'An application with this email is currrently under review. Please try again with another email.',
                                                                       'registration_form': registration_form})
            elif User.objects.filter(email=request.POST['email']).filter(is_active='True').exists():
                return render(request, 'wikodeApp/registration.html', {'form': UserCreationForm(),
                                                                       'same_email': 'This email is used before. Please use another email.',
                                                                       'registration_form': registration_form})
            else:
                registration_form.save()
                return render(request, 'wikodeApp/login.html', {'form': UserCreationForm(), 'success': 'Thank you for your application. Your account will be activated after reviewed carefully.'})
        else:
            return render(request, 'wikodeApp/registration.html', {'registration_form': registration_form})
    else:
        registration_form = ApplicationRegistrationForm()

    return render(request, 'wikodeApp/registration.html', {'registration_form': registration_form})


@login_required
def registrationRequests(request):
    if request.method == 'POST':
        approved_request = RegistrationApplication.objects.get(pk=request.POST['request_id'])
        approved_request.applicationStatus = '2'
        approved_request.save()
        random_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        user = User(username=approved_request.email,
                    first_name=approved_request.name,
                    last_name=approved_request.surname,
                    email=approved_request.email,
                    password=random_password)
        user.set_password(user.password)
        user.save()

        requests_list = RegistrationApplication.objects.filter(applicationStatus='1').order_by('applicationDate')
        requests_dict = {"registration_requests": requests_list, "password": random_password}
        return render(request, 'wikodeApp/registrationRequests.html', context=requests_dict)

    requests_list = RegistrationApplication.objects.filter(applicationStatus='1').order_by('applicationDate')
    requests_dict = {"registration_requests": requests_list}
    return render(request, 'wikodeApp/registrationRequests.html', context=requests_dict)


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('wikodeApp:homePage'))
            else:
                return HttpResponse("Your account is not active.")
        else:
            return render(request, 'wikodeApp/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password did not match.'})

    else:
        return render(request, 'wikodeApp/login.html', {})


@login_required
def userList(request):
    if request.method == 'POST':
        if 'user_id' in request.POST:
            removed_user = User.objects.get(pk=request.POST['user_id'])
            removed_user.is_active = False
            removed_user.save()
        elif 'admin_status' in request.POST:
            admin_user = User.objects.get(pk=request.POST['admin_status'])
            admin_user.is_superuser = not admin_user.is_superuser
            admin_user.userprofileinfo.save()

    users = User.objects.filter(is_active=True)
    cur_username = request.user.username
    admin_status = User.objects.filter(username=cur_username).values_list('is_superuser')
    return render(request, 'wikodeApp/userList.html', {'user_list': users, 'admin': admin_status[0][0]})


@login_required
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('wikodeApp:userLogin'))


@login_required
def getArticles(request):
    if request.method == 'POST':
        form = GetArticleForm(request.POST)

        if form.is_valid():
            createArticles(form.cleaned_data['article_topic'], form.cleaned_data['volume'])
            saved_count = Article.objects.all().count()
            return render(request, 'wikodeApp/articlesSaved.html', {'saved_count': saved_count})
    else:
        form = GetArticleForm()

    return render(request, 'wikodeApp/fetchArticles.html', {'form': form})
