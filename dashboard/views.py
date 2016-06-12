# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from authentication.views import login

# Create your views here.

def manager(request):
    """

    :param request:
    :return:
    """
    if request.user.is_superuser:
        args = {}
        args.update(csrf(request))
        args['username'] = auth.get_user(request).username
        # тут выполняется основная задача
    else:
        # отправляем на аутентификацию и проверяем пользователя
        login(request)

    return (render_to_response('manager.html', args))

def testpage(request):
    return (render_to_response('test.html', testpage))