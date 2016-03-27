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
from authentication.models import Bank, Account


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
    return redirect(return_path)

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
    args['userprofile'] = request.user
    args['banks'] = Bank.objects.all()
    args.update(csrf(request))
    return render_to_response('profile.html', args)

def public_profile(request, username, param):
    # Тут код публичного профиля
    public_profile = Account.objects.get(username=username)
    args = {}
    args['userprofile'] = request.user
    args['public_username'] = public_profile.username
    args['public_first_name'] = public_profile.first_name
    args['public_last_name'] = public_profile.last_name
    if public_profile.is_company == True:
        args['public_company_phone'] = public_profile.company_phone
        args['public_company_name'] = public_profile.company_name

    args.update(csrf(request))
    return render_to_response('public_profile.html', args)

def get_photo(request, username):
    # Тут код отдачи фотографии
    # HttpResponse.content = '/Volumes/Developer/Projects/TonerProject/media/profile/defaultprofileimage.jpg'
    return redirect(os.path.join(STATIC_URL, "profile/" + username + ".jpg"))


def change_user_info(request):
    if request.user.is_authenticated() and request.POST:
        # Пользователь аутентифицирован
        # необходимо выполнить валидацию каждого поля перед изменением
        user_for_change = request.user

        # username
        user_for_change.username = request.POST.get('userprofile_username')
        if len(user_for_change.username) < 6:
            return HttpResponse(u'Логин не может быть меньше 6 символов', content_type='text/html')
        if len(user_for_change.username) > 30:
            return HttpResponse(u'Логин не может быть больше 30 символов', content_type='text/html')
        if not user_for_change.username.isalnum():
            return HttpResponse(u'Логин может состоять только из букв и цифр', content_type='text/html')

        # email
        user_for_change.email = request.POST.get('userprofile_email')
        if len(user_for_change.email) < 10:
            return HttpResponse(u'Очень короткий email', content_type='text/html')
        if user_for_change.email.find('@') == -1 or user_for_change.email.find('.') == -1:
            return HttpResponse(u'Не верный email', content_type='text/html')

        # first_name
        user_for_change.first_name = request.POST.get('userprofile_first_name')
        if len(user_for_change.first_name) < 2:
            return HttpResponse(u'Слишком короткое Имя пользователя', content_type='text/html')
        if not user_for_change.first_name.isalpha():
            return HttpResponse(u'Имя пользователя может состоять только из букв', content_type='text/html')

        # last_name
        user_for_change.last_name = request.POST.get('userprofile_last_name')
        if len(user_for_change.last_name) < 2:
            return HttpResponse(u'Слишком короткая Фамилия пользователя', content_type='text/html')
        if not user_for_change.last_name.isalpha():
            return HttpResponse(u'Фамилия пользователя может состоять только из букв', content_type='text/html')

            # tag_line     не проверяется

        if request.POST.get('userprofile_is_company') == 'yes':
            user_for_change.is_company = True
            # company_name
            user_for_change.company_name = request.POST.get('userprofile_company_name')
            if len(user_for_change.company_name) < 4:
                return HttpResponse(u'Наименование организации не допустимо короткое', content_type='text/html')

            # company_boss_first_name
            user_for_change.company_boss_first_name = request.POST.get('userprofile_company_boss_first_name')
            if len(user_for_change.company_boss_first_name) < 2:
                return HttpResponse(u'Слишком короткое Имя руководителя', content_type='text/html')
            if not user_for_change.company_boss_first_name.isalpha():
                return HttpResponse(u'Имя пользователя может состоять только из букв', content_type='text/html')

            # company_boss_second_name
            user_for_change.company_boss_second_name = request.POST.get('userprofile_company_boss_second_name')
            if len(user_for_change.company_boss_second_name) < 2:
                return HttpResponse(u'Слишком короткое Отчество руководителя', content_type='text/html')
            if not user_for_change.company_boss_second_name.isalpha():
                return HttpResponse(u'Отчество руководителя может состоять только из букв', content_type='text/html')

            # company_boss_last_name
            user_for_change.company_boss_last_name = request.POST.get('userprofile_company_boss_last_name')
            if len(user_for_change.company_boss_last_name) < 2:
                return HttpResponse(u'Слишком короткая Фамилия руководителя', content_type='text/html')
            if not user_for_change.company_boss_last_name.isalpha():
                return HttpResponse(u'Фамилия руководителя может состоять только из букв', content_type='text/html')

            # company_name
            user_for_change.company_phone = request.POST.get('userprofile_company_phone')
            if len(user_for_change.company_phone) != 10:
                return HttpResponse(u'Телефон организации должен состоять из 10 цифр', content_type='text/html')
            if not user_for_change.company_phone.isdigit():
                return HttpResponse(u'Телефон должен состоять только из цифр', content_type='text/html')

            # company_address     не проверяется

            # company_inn
            user_for_change.company_inn = request.POST.get('userprofile_company_inn')
            if len(user_for_change.company_inn) != 10 and len(user_for_change.company_inn) != 12:
                return HttpResponse(u'ИНН организации должен состоять из 10 или 12 цифр', content_type='text/html')
            if not user_for_change.company_inn.isdigit():
                return HttpResponse(u'ИНН должен состоять только из цифр', content_type='text/html')

            # company_ogrn
            user_for_change.company_ogrn = request.POST.get('userprofile_company_ogrn')
            if len(user_for_change.company_ogrn) != 15:
                return HttpResponse(u'ОГРН организации должен состоять из 15 цифр', content_type='text/html')
            if not user_for_change.company_ogrn.isdigit():
                return HttpResponse(u'ОГРН должен состоять только из цифр', content_type='text/html')

            # company_okpo
            user_for_change.company_okpo = request.POST.get('userprofile_company_okpo')
            if len(user_for_change.company_okpo) != 9:
                return HttpResponse(u'ОКПО организации должен состоять из 9 цифр', content_type='text/html')
            if not user_for_change.company_okpo.isdigit():
                return HttpResponse(u'ОКПО должен состоять только из цифр', content_type='text/html')

            # company_okpo
            user_for_change.company_okato = request.POST.get('userprofile_company_okato')
            if len(user_for_change.company_okato) != 11:
                return HttpResponse(u'ОКАТО организации должен состоять из 9 цифр', content_type='text/html')
            if not user_for_change.company_okato.isdigit():
                return HttpResponse(u'ОКАТО должен состоять только из цифр', content_type='text/html')

            # user_bank_account
            user_for_change.user_bank_account = request.POST.get('userprofile_user_bank_account')
            if len(user_for_change.user_bank_account) != 20:
                return HttpResponse(u'Банковский счёт должен состоять из 20 цифр', content_type='text/html')
            if not user_for_change.user_bank_account.isdigit():
                return HttpResponse(u'Банковский счёт должен состоять только из цифр', content_type='text/html')

            # user_bank
            try:
                user_for_change.user_bank = Bank.objects.get(bank_name=request.POST.get('userprofile_user_bank'))
            except:
                return HttpResponse(u'Указаный банк не найден в БД', content_type='text/html')

        else:
            user_for_change.is_company = False


        # изменение профиля тут
        user_for_change.save()
        return HttpResponse(u'Данные успешно изменены', content_type='text/html')

    else:
        return HttpResponse(u'Bad User', content_type='text/html')
