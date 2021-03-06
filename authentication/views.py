# -*- coding: utf-8 -*-
import os
import sys
from django.contrib.auth import get_user_model
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.context_processors import csrf
import django.template.loader
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie
from TonerProject.settings import STATIC_URL
from authentication.models import Account
from contractor.models import Contractor, BANK
from TonerProject.settings import PROFILE_IMAGE_DEFAULT_NAME, PROFILE_IMAGE_DIR


def load_login_form(request):
    return HttpResponse(django.template.loader.get_template("login.html").render(), content_type='text/html')


def load_register_form(request):
    return HttpResponse(django.template.loader.get_template("register.html").render(), content_type='text/html')


@ensure_csrf_cookie
def login(request):
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponse(u'Ok', content_type='text/html')
        else:
            return HttpResponse(u'Неверный логин/пароль', content_type='text/html')
    else:
        return HttpResponse(u'Ошибка авторизации!', content_type='text/html')


def logout(request):
    return_path = request.META.get('HTTP_REFERER', '/')
    auth.logout(request)
    return redirect(return_path)


@ensure_csrf_cookie
def register(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        # Проверка на уникальность nickname
        try:
            if Account.objects.get(nickname=request.POST.get('nickname')):
                return HttpResponse(u'Nickname is not unique', content_type='text/html')
        except Account.DoesNotExist:
            # Проверка на уникальность username
            try:
                if Account.objects.get(username=request.POST.get('username')):
                    return HttpResponse(u'Username is not unique', content_type='text/html')

            except Account.DoesNotExist:
                # Имя не занято
                if request.POST.get('nickname') == request.POST.get('username'):
                    return HttpResponse(u'В целях безопастности никнейм и логих не должны совпадать',
                                        content_type='text/html')
                try:
                    # Проверка на уникальность email
                    if Account.objects.get(email=request.POST.get('email')):
                        return HttpResponse(u'Email is not unique', content_type='text/html')
                except Account.DoesNotExist:
                    # email не использован

                    # Тут проверка на совпадение паролей
                    if request.POST.get('password') != request.POST.get('password-confirm'):
                        return HttpResponse(u'Bad Password or Passwords are different', content_type='text/html')

                    # Валидация выше - если все удачно создаем пользователя
                    new_user = Account.objects.create_user(username=request.POST.get('username'),
                                                           password=request.POST.get('password-confirm'),
                                                           email=request.POST.get('email'), )
                    new_user.save()

                    # Сразу же логинимся
                    user = auth.authenticate(username=request.POST.get('username'),
                                             password=request.POST.get('password-confirm'), )
                    if user is not None:
                        auth.login(request, user)
                        return HttpResponse(u'Ok', content_type='text/html')
                    else:
                        return HttpResponse(u'Can\'t authenticate new user' + user, content_type='text/html')
                except:
                    return HttpResponse(u'login error', content_type='text/html')

            except:
                return HttpResponse(sys.exc_info(), content_type='text/html')
    else:
        return HttpResponse(u'Bad POST request', content_type='text/html')
    return HttpResponse(u'Unknown error', content_type='text/html')


    # render_to_response(return_path, args)


def dispatch_user(request, nickname, **kwargs):
    user_for_profile = get_object_or_404(get_user_model(), nickname=nickname)
    if user_for_profile == request.user:
        return profile(request)
    else:
        return public_profile(request, nickname)


@ensure_csrf_cookie
def profile(request):
    # Тут код личного профиля
    args = {'user_profile': request.user}
    try:
        args['banks'] = Contractor.objects.filter(type__name=BANK)
    except Contractor.DoesNotExist:
        return HttpResponse(
            u'Ошибка в view.profile. Не могу прочитать список банков',
            content_type='text/html')
    if request.user.contractor_id is not None:
        args['contractor'] = Contractor.objects.get(id=request.user.contractor_id)
    args.update(csrf(request))
    return render_to_response('profile.html', args)


@ensure_csrf_cookie
def public_profile(request, nickname):
    # Тут код публичного профиля
    try:
        _public_profile = Account.objects.get(nickname=nickname)
        args = {'user_profile': request.user,
                'public_phone': _public_profile.phone,
                'public_nickname': _public_profile.nickname,
                'public_first_name': _public_profile.first_name,
                'public_last_name': _public_profile.last_name,
                }
        if _public_profile.is_company:
            try:
                args['public_contractor_name'] = Contractor.objects.get(id=_public_profile.contractor_id).name
            except Contractor.DoesNotExist:
                args['public_contractor_name'] = "Ошибка БД. Обратитесь к администратору"
                # Код отправки баг репорта администратору
                return HttpResponse(
                    u'Ошибка в view.public_profile. Не могу получить доступ к учетной записи организации в БД',
                    content_type='text/html')
        else:
            args['public_contractor_name'] = "Частное лицо"
    except Account.DoesNotExist:
        # Баг репорт.
        return HttpResponse(u'Ошибка в view.public_profile. Не могу получить доступ к учетной записи пользователя в БД',
                            content_type='text/html')

    args.update(csrf(request))
    return render_to_response('public_profile.html', args)


def get_photo(request, nickname):
    # Тут код отдачи фотографии
    # HttpResponse.content = '/Volumes/Developer/Projects/TonerProject/media/profile/defaultprofileimage.jpg'
    try:
        user = Account.objects.get(nickname=nickname)
    except:
        return redirect(os.path.join(STATIC_URL, PROFILE_IMAGE_DEFAULT_NAME))
    return redirect(os.path.join(STATIC_URL, PROFILE_IMAGE_DIR + user.get_photo()))


def change_user_info(request):
    if request.user.is_authenticated() and request.POST:
        # Пользователь аутентифицирован
        # необходимо выполнить валидацию каждого поля перед изменением
        user_for_change = request.user

        # nickname
        user_for_change.username = request.POST.get('userprofile_nickname')
        if len(user_for_change.nickname) < 5:
            return HttpResponse(u'Никнейм не может быть меньше 5 символов', content_type='text/html')
        if len(user_for_change.nickname) > 30:
            return HttpResponse(u'Никнейм не может быть больше 30 символов', content_type='text/html')

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

        # phone
        user_for_change.phone = request.POST.get('userprofile_phone')
        if len(user_for_change.phone) != 10:
            return HttpResponse(u'Контактный телефон должен состоять из 10 цифр', content_type='text/html')
        if not user_for_change.phone.isdigit():
            return HttpResponse(u'Контактный телефон должен состоять только из цифр', content_type='text/html')

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
        user_for_change.tagline = request.POST.get('userprofile_tagline')

        if request.POST.get('userprofile_is_company') == 'yes' or request.POST.get('userprofile_is_company') == 'on':
            user_for_change.is_company = True
            if user_for_change.contractor_id is None:
                try:
                    contractor_for_change = Contractor.objects.create()
                    user_for_change.contractor_id = contractor_for_change
                    user_for_change.is_company = True
                    user_for_change.contractor.save()
                except:
                    user_for_change.is_company = True
        else:
            user_for_change.is_company = False
            if user_for_change.contractor:
                try:
                    contractor_for_change = Contractor.objects.get(id=user_for_change.contractor_id)
                    contractor_for_change.delete()
                    user_for_change.contractor = None
                except Contractor.DoesNotExist:
                    user_for_change.contractor = None
        # изменение профиля тут
        user_for_change.save()
        return HttpResponse(u'Ok', content_type='text/html')

    else:
        return HttpResponse(u'Bad change User data', content_type='text/html')


def change_contractor_info(request):
    if request.user.is_authenticated() and request.POST:
        # Пользователь аутентифицирован
        # необходимо выполнить валидацию каждого поля перед изменением
        user_for_change = request.user

        try:
            bank = Contractor.objects.get(name=request.POST.get('contractor_bank'))
        except:
            return HttpResponse(u'Указаный банк не найден в БД', content_type='text/html')

        # name
        if len(request.POST.get('company_name')) < 4:
            return HttpResponse(u'Наименование организации не допустимо короткое', content_type='text/html')
        # boss_first_name
        if len(request.POST.get('company_boss_first_name')) < 2:
            return HttpResponse(u'Слишком короткое Имя руководителя', content_type='text/html')
        if not request.POST.get('company_boss_first_name').isalpha():
            return HttpResponse(u'Имя пользователя может состоять только из букв', content_type='text/html')
        # boss_second_name
        if len(request.POST.get('company_boss_second_name')) < 2:
            return HttpResponse(u'Слишком короткое Отчество руководителя', content_type='text/html')
        if not request.POST.get('company_boss_second_name').isalpha():
            return HttpResponse(u'Отчество руководителя может состоять только из букв', content_type='text/html')
        # boss_last_name
        if len(request.POST.get('company_boss_last_name')) < 2:
            return HttpResponse(u'Слишком короткая Фамилия руководителя', content_type='text/html')
        if not request.POST.get('company_boss_last_name').isalpha():
            return HttpResponse(u'Фамилия руководителя может состоять только из букв', content_type='text/html')
        # phone
        if len(request.POST.get('company_phone')) != 10:
            return HttpResponse(u'Телефон организации должен состоять из 10 цифр', content_type='text/html')
        if not request.POST.get('company_phone').isdigit():
            return HttpResponse(u'Телефон должен состоять только из цифр', content_type='text/html')
        # address
        if len(request.POST.get('company_address')) > 100:
            return HttpResponse(u'Адрес организации не должен превышать 100 знаков', content_type='text/html')
        # inn
        if len(request.POST.get('company_inn')) != 10 and len(request.POST.get('company_inn')) != 12:
            return HttpResponse(u'ИНН организации должен состоять из 10 или 12 цифр', content_type='text/html')
        if not request.POST.get('company_inn').isdigit():
            return HttpResponse(u'ИНН должен состоять только из цифр', content_type='text/html')
        # ogrn
        if len(request.POST.get('company_ogrn')) != 15:
            return HttpResponse(u'ОГРН организации должен состоять из 15 цифр', content_type='text/html')
        if not request.POST.get('company_ogrn').isdigit():
            return HttpResponse(u'ОГРН должен состоять только из цифр', content_type='text/html')
        # okpo
        if len(request.POST.get('company_okpo')) != 9:
            return HttpResponse(u'ОКПО организации должен состоять из 9 цифр', content_type='text/html')
        if not request.POST.get('company_okpo').isdigit():
            return HttpResponse(u'ОКПО должен состоять только из цифр', content_type='text/html')
        # okato
        if len(request.POST.get('company_okato')) != 11:
            return HttpResponse(u'ОКАТО организации должен состоять из 11 цифр', content_type='text/html')
        if not request.POST.get('company_okato').isdigit():
            return HttpResponse(u'ОКАТО должен состоять только из цифр', content_type='text/html')
        # account
        if len(request.POST.get('company_account')) != 20:
            return HttpResponse(u'Банковский счёт должен состоять из 20 цифр', content_type='text/html')
        if not request.POST.get('company_account').isdigit():
            return HttpResponse(u'Банковский счёт должен состоять только из цифр', content_type='text/html')


            # try:
            # Создаем новый объект
            #    contractor_for_change = contractor.objects.create()
            # contractor_for_change.save()
            # except:
            #    return HttpResponse(u'Не удается создать организацию', content_type='text/html')
        try:
            contractor_for_change = Contractor.objects.get(id=request.user.contractor_id)
        except Contractor.DoesNotExist:
            try:
                # Создаем новый объект
                contractor_for_change = Contractor.objects.create()
                contractor_for_change.save()
            except:
                return HttpResponse(u'change_contractor_info: Не удается создать организацию в БД',
                                    content_type='text/html')
        # Валидация пройдена изменяем запись в БД
        # name
        contractor_for_change.name = request.POST.get('company_name')
        # boss_first_name
        contractor_for_change.boss_first_name = request.POST.get('company_boss_first_name')
        # boss_second_name
        contractor_for_change.boss_second_name = request.POST.get('company_boss_second_name')
        # boss_last_name
        contractor_for_change.boss_last_name = request.POST.get('company_boss_last_name')
        # phone
        contractor_for_change.phone = request.POST.get('company_phone')
        # address
        contractor_for_change.address = request.POST.get('company_address')
        # inn
        contractor_for_change.inn = request.POST.get('company_inn')
        # ogrn
        contractor_for_change.ogrn = request.POST.get('company_ogrn')
        # okpo
        contractor_for_change.okpo = request.POST.get('company_okpo')
        # okato
        contractor_for_change.okato = request.POST.get('company_okato')
        # account
        contractor_for_change.account = request.POST.get('company_account')
        # user_bank
        contractor_for_change.bank = bank

        # изменение профиля тут
        user_for_change.contractor = contractor_for_change
        user_for_change.is_company = True
        user_for_change.save()
        contractor_for_change.save()
        return HttpResponse(u'Ok', content_type='text/html')
    else:
        return HttpResponse(u'Bad change contractor data', content_type='text/html')
