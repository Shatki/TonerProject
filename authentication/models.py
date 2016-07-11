from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from system.validators import numeric, phone, alphanumeric


class Bank(models.Model):
    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'
        db_table = 'bank'

    name = models.CharField(verbose_name=u'Наименование банка', unique=True, max_length=100, db_index=True, blank=False)
    address = models.CharField(verbose_name=u'Адрес банка', max_length=100)  # адрес банка
    account = models.CharField(verbose_name=u'Корреспондентский счёт', unique=True, max_length=20, db_index=True,
                               validators=[numeric])  # Кор счет
    bik = models.CharField(verbose_name=u'БИК', unique=True, max_length=9, db_index=True,
                           validators=[numeric])  # Кор счет
    # для отображения в списках
    def __str__(self):
        return self.name


class Company(models.Model):
    #### ДАННЫЕ Организации #########
    # Наименование компании - не обязательна для физ лиц
    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        db_table = 'company'

    # numeric = RegexValidator(r'^[0-9]*$', message=u'Только цифровые символы допустимы.')
    name = models.CharField(verbose_name=u'Наименование компании', max_length=100, blank=True, null=True)
    boss_first_name = models.CharField(verbose_name=u'Имя руководителя', max_length=40, blank=True, null=True)  # Имя
    boss_second_name = models.CharField(verbose_name=u'Отчество руководителя', max_length=40, blank=True,
                                        null=True)  # Отчество
    boss_last_name = models.CharField(verbose_name=u'Фамилия руководителя', max_length=40, blank=True,
                                      null=True)  # Фамилия
    phone = models.CharField(verbose_name=u'Контактный телефон', max_length=10, validators=[phone], null=True)
    inn = models.CharField(verbose_name=u'ИНН', unique=True, max_length=12, validators=[numeric], null=True)  # ИНН
    ogrn = models.CharField(verbose_name=u'ОГРН', unique=True, max_length=15, validators=[numeric], null=True)  # ОГРН
    okpo = models.CharField(verbose_name=u'ОКПО', max_length=9, validators=[numeric], null=True)  # ОКПО
    okato = models.CharField(verbose_name=u'ОКАТО', max_length=11, validators=[numeric], null=True)  # ОКАТО
    address = models.CharField(verbose_name=u'Адрес организации', max_length=100, null=True)
    bank = models.ForeignKey(Bank, verbose_name=u'Банк', blank=True, null=True)
    bank_account = models.CharField(verbose_name=u'Банковский счёт', max_length=20, validators=[numeric],
                                    null=True)  # счет

    def __str__(self):
        return self.name

    def get_boss_full_name(self):
        return ' '.join([self.boss_first_name, self.boss_second_name, self.boss_last_name])

    def get_boss_short_name(self):
        return ' '.join([self.boss_first_name, self.boss_second_name])

# Класс менеджера должен переопределить методы create_user() и create_superuser().
class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('Имя пользователя обязательно')

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
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'account'
    #### ДАННЫЕ ПОЛЬЗОВАТЕЛЯ #########
    # username нам  необходим для отображении записей и страницы действий
    nickname = models.CharField(verbose_name=u'Имя пользователя в системе', unique=True, max_length=30, db_index=True,
                                validators=[alphanumeric])
    username = models.CharField(verbose_name=u'Логин входа в систему', unique=True, max_length=30, db_index=True,
                                validators=[alphanumeric])
    #Авторизация будет происходить по E-mail
    email = models.EmailField(verbose_name=u'Электронная почта', unique=True, max_length=255)
    # Имя - не является обязательным
    first_name = models.CharField(verbose_name=u'Имя пользователя', max_length=40, blank=True, null=True)
    # Фамилия - также не обязательна
    last_name = models.CharField(verbose_name=u'Фамилия пользователя', max_length=40, blank=True, null=True)
    # слоган или статус - куда же без него. Наследство от соц. сетей
    tagline = models.CharField(verbose_name=u'Статус', max_length=140, blank=True, null=True)
    photo = models.FilePathField(verbose_name=u'Аватар', blank=True, null=True,
                                      default='profile/defaultprofileimage.jpg')
    phone = models.CharField(verbose_name=u'Сотовый телефон', max_length=10, validators=[phone], null=True)
    company = models.ForeignKey(Company, verbose_name=u'Организация', blank=True, null=True)

    #### АТРИБУТЫ #########
    # Атрибут суперпользователя
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, null=False)
    is_company = models.BooleanField(default=False, null=False)

    # Сохраняем время создания и обновления аккаунта пользователя.
    # Устанавливая auto_now_add=True, мы говорим Джанго автоматически
    # ставить время при создании, причем далее поле будет нередактируемым.
    #  Аналогично и auto_now=True, разница в том, что поле каждый раз обновляется с обновлением объекта
    date_joined = models.DateTimeField(verbose_name=u'Дата создания', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name=u'Последнее обновление', auto_now=True)



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
