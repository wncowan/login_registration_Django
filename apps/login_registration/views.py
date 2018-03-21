# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from django.contrib import messages
from .models import User
# Create your views here.
def index(request):
    users = User.objects.all()
    context = {
        "all_users" : users
    }
    return render(request, "login_registration/index.html", context)

def create(request):
    print('entered create')
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], confirm_password=request.POST['confirm_password'])
        request.session['user_id'] = new_user.first_name
        request.session['action'] = "registered"
        print(request.session['user_id'])
        return redirect('/success')

def login(request):
    print('entered login')
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.filter(email=request.POST['email'])[0].first_name
        request.session['action'] = "logged in"
        return redirect('/success')

    return redirect('/')

def delete(request):
    print('entered delete')
    b = User.objects.all()
    b.delete()
    return redirect('/')    

def success(request):
    print('entered success')
    return render(request, 'login_registration/success.html')
