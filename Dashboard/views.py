from django.http import HttpResponse
from django.shortcuts import render, redirect
from API.FirebaseConsole import find_admin_user
from django.contrib import messages


def home(request):
    try:
        if request.session['username']:
            print('ALL OK')
        else:
            return redirect('Dashboard:login')
    except:
        return redirect('Dashboard:login')
    return render(request, 'dashboard/dashboard.html')

def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        admin_user = find_admin_user(username)

        if admin_user == None:
            messages.add_message(request, messages.ERROR, 'User Not Found')
            return render(request, 'Login/login.html')
        else:
            if admin_user['password'] == password:
                request.session['username'] = username
                return redirect('Dashboard:home')
            else:
                messages.add_message(request, messages.ERROR, 'Wrong Credentials')
            return render(request, 'Login/login.html')


    else:
        return render(request, 'Login/login.html')

def check_login(request):
    try:
        if request.session['username']:
            print('ALL OK')
        else:
            return redirect('Dashboard:login')
    except:
        return redirect('Dashboard:login')