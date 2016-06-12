from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


class Bank(models.Model):
    # alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message=u'Только буквенноцифровые символы допустимы.')
    numeric = RegexValidator(r'^[0-9]*$', message=u'Только цифровые символы допустимы.')
    bank_name = models.CharField(unique=True, max_length=100, db_index=True, blank=False)
    bank_address = models.CharField(max_length=100)  # адрес банка
    bank_account = models.CharField(unique=True, max_length=20, db_index=True, validators=[numeric])  # Кор счет
    bank_bik = models.CharField(unique=True, max_length=9, db_index=True, validators=[numeric])  # Кор счет
    # для отображения в списках
    def __str__(self):
        return self.bank_name

# Класс менеджера должен переопределить методы create_user() и create_superuser().
class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Имя пользователя обязательно')

        account = self.model(username=username)
        if kwargs.get('email'):
            account.email = kwargs.get('email'),
        if kwargs.get('phone'):
            account.company_phone = kwargs.get('phone')

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
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message=u'Только буквенноцифровые символы допустимы.')
    numeric = RegexValidator(r'^[0-9]*$', message=u'Только цифровые символы допустимы.')
    phone = RegexValidator(regex='^\d{10}$', message=u'Укажите правильный номер телефона')

    #### ДАННЫЕ ПОЛЬЗОВАТЕЛЯ #########
    # username нам  необходим для отображении записей и страницы действий
    username = models.CharField(verbose_name=u'Логин', unique=True, max_length=30, db_index=True,
                                validators=[alphanumeric])
    #Авторизация будет происходить по E-mail
    email = models.EmailField(verbose_name=u'Электронная почта', unique=True, max_length=255)
    # Имя - не является обязательным
    first_name = models.CharField(verbose_name=u'Имя пользователя', max_length=40, blank=True, null=True)
    # Фамилия - также не обязательна
    last_name = models.CharField(verbose_name=u'Фамилия пользователя', max_length=40, blank=True, null=True)
    # слоган или статус - куда же без него. Наследство от соц. сетей
    tagline = models.CharField(verbose_name=u'Статус', max_length=140, blank=True, null=True)
    user_photo = models.FilePathField(verbose_name=u'Аватар', blank=True, null=True,
                                  default='/profile/defaultprofileimage.jpg')

    #### ДАННЫЕ Организации #########
    # Наименование компании - не обязательна для физ лиц
    company_name = models.CharField(verbose_name=u'Наименование компании', max_length=100, blank=True, null=True)
    company_boss_first_name = models.CharField(max_length=40, blank=True, null=True)  # Имя
    company_boss_second_name = models.CharField(max_length=40, blank=True, null=True)  # Отчество
    company_boss_last_name = models.CharField(max_length=40, blank=True, null=True)  # Фамилия
    company_inn = models.CharField(unique=True, max_length=12, validators=[numeric], null=True)  # ИНН
    company_ogrn = models.CharField(unique=True, max_length=15, validators=[numeric], null=True)  # ОГРН
    company_okpo = models.CharField(max_length=9, validators=[numeric], null=True)  # ОКПО
    company_okato = models.CharField(max_length=11, validators=[numeric], null=True)  # ОКАТО
    company_address = models.CharField(max_length=100, null=True)
    company_phone = models.CharField(max_length=10, validators=[phone], null=True)
    user_bank = models.ForeignKey(Bank, blank=True, null=True)
    user_bank_account = models.CharField(max_length=20, validators=[numeric], null=True)  # счет

    #### АТРИБУТЫ #########
    # Атрибут суперпользователя
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_company = models.BooleanField(default=False, null=False)

    # Сохраняем время создания и обновления аккаунта пользователя.
    # Устанавливая auto_now_add=True, мы говорим Джанго автоматически
    # ставить время при создании, причем далее поле будет нередактируемым.
    #  Аналогично и auto_now=True, разница в том, что поле каждый раз обновляется с обновлением объекта
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)



    objects = AccountManager()

    # Имя пользователя мы будем выводить в нескольких местах.
    #  Так как это поле необязательно, мы включаем его в список REQUIRED_FIELDS.
    #  Обычно достаточно указать required=True, но так как мы заменяем модель User,
    #  Джанго требует явно определить это поле.
    # логинимся по email
    USERNAME_FIELD = 'username'
    # обязательное поле
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_boss_full_name(self):
        return ' '.join([self.company_boss_first_name, self.company_boss_second_name, self.company_boss_last_name])

    def get_boss_short_name(self):
        return ' '.join([self.company_boss_first_name, self.company_boss_second_name])

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_photo(self):
        return self.user_photo

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
