# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse # HttpResponse not in use
from .models import User

# Login + Registration

def index(request):
    if 'id' in request.session:
        return redirect('/success')
    return render(request, 'login_registration/index.html')

def login(request):
    if request.method == 'GET':
        if 'id' in request.session:
            return redirect('/success')
        return render(request, 'login_registration/login.html')
    if request.method == 'POST':
        # check if login is valid
        if User.objects.login(request)[0] is True:
            return redirect('/success')
        return redirect('/login')

def register(request):
    if request.method == 'GET':
        if 'id' in request.session:
            return redirect('/success')
        return render(request, 'login_registration/register.html')
    if request.method == 'POST':
        # check if registration data is valid
        if User.objects.validate(request) is True:
            # create user
            User.objects.register(request)
            # login and update 'request' 
            request = User.objects.login(request)[1]
            return success(request)
        return redirect('/register')

# redirect for successful login
def success(request):
    # check if user is logged in
    if 'id' in request.session: 
        return redirect('/dashboard')
    return redirect('/')

def logout(request):
    #clear session data
    for data in request.session.keys(): 
        del request.session[data]
    return redirect('/')

# Dashbord

def dashboard(request):
    if 'id' in request.session:
        if request.session['level'] == 9:
            return redirect('/dashboard/admin')
        context = {
            'users' : User.objects.render_users()
        }
        return render(request, 'login_registration/dashboard.html', context)
    return redirect('/')

def dashboard_admin(request):
    if 'id' in request.session:
        if request.session['level'] != 9:
            return redirect('/dashboard')
        context = {
            'users' : User.objects.render_users()
        }
        return render(request, 'login_registration/dashboard.html', context)
    return redirect('/')

# Development

def reset(request):
    # clear user db
    User.objects.cleardb() # uncomment function in models.py
    # redirect to logout to complete reset
    return redirect('/logout') 
