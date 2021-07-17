from web.forms import UserRegistrationForm
from django.contrib.auth import authenticate
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, get_user_model, login, logout
from . models import *

def home(request):
    return render(request, 'web/home.html')


def login_redirect(request):
    title = request.user.title

    if title == "judge":
        return redirect('compi-scoresheet-main')
    else:
        return redirect('web-home')

def web_login(request):
    context = {
        'title':'Login'
    }
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            context['header'] = 'Response'
            context['card_title'] = 'Login Failed!'
            context['message'] = 'Email or password is incorrect!'
            context['linkto'] = 'web-login'
            return render(request, 'web/response.html', context)
        login(request, user)
        # print(user.title)
        return redirect('web-login-redirect')

    return render(request, 'web/login.html')

def web_logout(request):
    logout(request)
    return redirect('web-home')
