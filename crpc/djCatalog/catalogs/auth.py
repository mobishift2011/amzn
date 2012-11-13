# -*- coding: utf-8 -*-
from django.contrib.auth import login as signin, logout as signout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from mongoengine.django.auth import User
from mongoengine.django.auth import MongoEngineBackend

def loginHandle(request):
    if request.method == "GET":
        if request.user.is_authenticated():
            return redirect('/admin')
        return render(request, 'login.html')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'devadmin':
            user, is_new = User.objects.get_or_create(username='devadmin')
            if is_new:
                user.set_password('tempfavbuy88')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            if user.check_password(password):
                user.backend = 'mongoengine.django.auth.MongoEngineBackend'
                signin(request, user)
                request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
                return redirect('/admin')
        return render(request, 'login.html', {'login_failed': True})

def logoutHandle(request):
    if request.user:
        return HttpResponse(request.user.username)
    else:
        return HttpResponse('no user to logout')