# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm

def home_page(request):
    args = {}
    args.update(csrf(request))
    args['username'] = auth.get_user(request).username
    args['form'] = UserCreationForm()
    return render_to_response('homepage.html', args)

