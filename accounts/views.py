from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LoginForm
from .models import User
import json
import random
# from twilio.rest import Client
from django.conf import settings
from django.http import HttpResponse
from django.conf import settings

from rental.models import Car

# Create your views here.

def log_in(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            try:
                if User.objects.get(username=username).is_active:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        context['username'] = username
                        context['password'] = password
                        context['userId'] = user.id

                        login(request, user)
                        return redirect('rental/')
                    else:
                        context['msg'] = 'Invalid username or password.'
                        context['msg_type'] = 'err'
                else:
                    context['msg'] = 'Your account is not activated yet.'
                    context['msg_type'] = 'err'
            except Exception as e:
                print(e)
                context['msg'] = 'This username is not registered yet.'
                context['msg_type'] = 'err'
        else:
            errors = json.dumps(form.errors)
            errors = json.loads(errors)
            text = "\n".join([value[0] for key, value in errors.items()])
            context['msg'] = text
            context['msg_type'] = 'err'
    return render(request, 'registration/login.html')


def register(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            print(username)
            form.save()
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            return render(request, 'registration/login.html')
        else:
            errors = json.dumps(form.errors)
            errors = json.loads(errors)
            text = "\n".join([value[0] for key, value in errors.items()])
            context['msg'] = text
            context['msg_type'] = 'err'
            print(text)
    return render(request, 'registration/register.html')


# def otp(request):
#     if request.method == 'POST':
#         otp_number = request.POST['otp']
#         try:
#             # print(otp_number, request.POST['mobile'])
#             # OTP.objects.get(otp_number=otp_number, otp_mobile=request.POST['mobile'])
#             user = authenticate(username=request.POST['username'], password=request.POST['password'])
#             login(request, user)
#             return redirect('panel:index')
#         except Exception as e:
#             print(e)
#             return redirect('login')

