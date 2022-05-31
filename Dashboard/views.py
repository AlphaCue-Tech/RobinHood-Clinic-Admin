from django.http import HttpResponse
from django.shortcuts import render
from API.FirebaseConsole import find_user


def home(request):

    return render(request, 'Login/login.html')
