# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie


def loadloginform(request):
    return HttpResponse(get_template("login.html").render(), content_type='text/html')

def loadregisterform(request):
    return HttpResponse(get_template("register.html").render(), content_type='text/html')


@ensure_csrf_cookie
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
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
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect(return_path)
        else:
            args['form'] = newuser_form
    return render_to_response(return_path, args)
