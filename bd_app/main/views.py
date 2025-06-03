from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login, logout, authenticate

def index(request):
    return render(request, "main/home.html")

def login(request):
    return render(request, "main/login.html")
