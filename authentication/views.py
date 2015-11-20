# -*- coding: utf-8 -*-
import os
from django.contrib.auth import get_user_model
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from TonerProject.settings import STATIC_URL


def loadloginform(request):
    return HttpResponse(get_template("login.html").render(), content_type='text/html')

def loadregisterform(request):
    return HttpResponse(get_template("register.html").render(), content_type='text/html')


@ensure_csrf_cookie
def login(request):
    if request.POST:
        login = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=login, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse('ok', content_type='text/html')
        else:
            return HttpResponse('Неверный логин/пароль', content_type='text/html')
    else:
        return HttpResponse('Ошибка авторизации!', content_type='text/html')


def logout(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(return_path)  #потом переделать

def register(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    args = {}
    args.update(csrf(request))
    # args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(email=newuser_form.cleaned_data['email'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect(return_path)
        else:
            args['form'] = newuser_form
    return render_to_response(return_path, args)

def dispatch_user(request, username, **kwargs):
    user_for_profile = get_object_or_404(get_user_model(), username=username)
    if user_for_profile == request.user:
        return profile(request, username, kwargs)
    else:
        return public_profile(request, username, kwargs)

def profile(request, username, param):
    # Тут код личного профиля
    args = {}
    args['username'] = request.user.username
    args.update(csrf(request))
    return render_to_response('profile.html', args)

def public_profile(request, username, param):
    # Тут код публичного профиля
    return HttpResponse(u'<http>Public profile of user: %s </http>' % username, content_type='text/html')

def get_photo(request, username):
    # Тут код отдачи фотографии
    # HttpResponse.content = '/Volumes/Developer/Projects/TonerProject/media/profile/defaultprofileimage.jpg'
    return redirect(os.path.join(STATIC_URL, "profile/" + username + ".jpg"))
