from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from ForumsApp.Forms import *


class LoginView(View):
    def get(self,request):
        form=LoginForm()
        return render(
            request,
            'login.html',
            {'form': form},
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('ForumsApp:allQuestions')
            else:
                messages.error(request, "Invalid credentials")
        return render(
            request,
            'login.html',
            {'form': form},
        )

class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(
            request,
            'signup.html',
            {'form': form},
        )
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('ForumsApp:allQuestions')
            else:
                messages.error(request, "Invalid credentials")

            return render(
                request,
                'signup.html',
                {'form': form},
            )

def logout_user(request):
    UpdateLoginTimeView.updateTime(request)
    logout(request)
    return redirect('ForumsApp:login')

class UpdateLoginTimeView(View):

    def updateTime(request):
        userdetails=User.objects.get(id=request.user.id)
        userdetails.last_login=datetime.now()
        userdetails.save()
