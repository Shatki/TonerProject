# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
# from django.contrib import auth
from django.template.context_processors import csrf
# from django.template.loader import get_template
# from authentication.models import Account
from contractor.models import Contractor
from authentication.views import login
from django.views.decorators.csrf import ensure_csrf_cookie


# from TonerProject.settings import STATIC_URL


# Create your views here.

@ensure_csrf_cookie
def dashboard(request):
    if request.user.is_authenticated():
        # Тут код личного профиля
        args = {}
        args['userprofile'] = request.user
        args['banks'] = Contractor.objects.filter(type='Банк')
        args.update(csrf(request))
        return render_to_response('dashboard.html', args)
    else:
        # отправляем на аутентификацию и проверяем пользователя
        return login(request)


def testpage(request):
    return render_to_response('test.html', testpage)
