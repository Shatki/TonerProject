# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from TonerProject.validators import phone, alphanumeric
from contractor.models import Contractor


# Класс менеджера должен переопределить методы create_user() и create_superuser().
class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('имя пользователя обязательно')

        account = self.model(username=username)
        if kwargs.get('email'):
            account.email = kwargs.get('email')
        if kwargs.get('nickname'):
            account.nickname = kwargs.get('nickname')

        account.set_password(password)
        account.is_staff = False
        account.is_company = False
        account.save(using=self._db)

        return account

    def create_superuser(self, username, password, **kwargs):
        account = self.create_user(username, password, **kwargs)
        account.is_superuser = True
        account.is_admin = True
        account.is_staff = True
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        db_table = 'account'

    #### ДАННЫЕ ПОЛЬЗОВАТЕЛЯ #########
    # username нам  необходим для отображении записей и страницы действий
    nickname = models.CharField(verbose_name=u'имя пользователя в системе', unique=True, max_length=30, db_index=True,
                                validators=[alphanumeric])
    username = models.CharField(verbose_name=u'логин входа в систему', unique=True, max_length=30, db_index=True,
                                validators=[alphanumeric])
    # Авторизация будет происходить по E-mail
    email = models.EmailField(verbose_name=u'электронная почта', unique=True, max_length=255)
    # Имя - не является обязательным
    first_name = models.CharField(verbose_name=u'имя пользователя', max_length=40, blank=True, null=True)
    # Фамилия - также не обязательна
    last_name = models.CharField(verbose_name=u'фамилия пользователя', max_length=40, blank=True, null=True)
    # слоган или статус - куда же без него. Наследство от соц. сетей
    tagline = models.CharField(verbose_name=u'статус', max_length=140, blank=True, null=True)
    photo = models.FilePathField(verbose_name=u'Аватар', blank=True, null=True,
                                 default='defaultprofileimage.jpg')
    phone = models.CharField(verbose_name=u'сотовый телефон', max_length=10, validators=[phone], null=True)
    contractor = models.ForeignKey(Contractor, verbose_name=u'организация', blank=True, null=True,
                                   related_name='account_contractor')

    # Атрибут суперпользователя
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_company = models.BooleanField(default=False, null=False)

    # Сохраняем время создания и обновления аккаунта пользователя.
    # Устанавливая auto_now_add=True, мы говорим Джанго автоматически
    # ставить время при создании, причем далее поле будет нередактируемым.
    #  Аналогично и auto_now=True, разница в том, что поле каждый раз обновляется с обновлением объекта
    date_joined = models.DateTimeField(verbose_name=u'дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'последнее обновление', auto_now=True)

    objects = AccountManager()

    # Имя пользователя мы будем выводить в нескольких местах.
    #  Так как это поле необязательно, мы включаем его в список REQUIRED_FIELDS.
    #  Обычно достаточно указать required=True, но так как мы заменяем модель User,
    #  Джанго требует явно определить это поле.
    # логинимся по email
    USERNAME_FIELD = 'username'
    # обязательное поле
    REQUIRED_FIELDS = ['nickname', 'email', ]

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_photo(self):
        return self.photo

    def get_company(self):
        if self.company is not None:
            return self.company.name
        else:
            return 'Частное лицо'
