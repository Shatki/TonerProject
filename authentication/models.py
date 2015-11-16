from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator


# Класс менеджера должен переопределить методы create_user() и create_superuser().
class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('User must have a valid email address.')
        if not kwargs.get('username'):
            raise ValueError('User must have a valid username.')

        account = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        account.set_password(password)
        account.is_staff = False
        account.is_company = False
        account.save(using=self._db)

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)
        account.is_superuser = True
        account.is_admin = True
        account.is_staff = True
        account.save(using=self._db)
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message=u'Только буквенноцифровые символы допустимы.')

    # username нам  необходим для отображении записей и страницы действий
    username = models.CharField(unique=True, max_length=30, db_index=True, validators=[alphanumeric])

    #Авторизация будет происходить по E-mail
    email = models.EmailField(verbose_name=u'Электронная почта', unique=True, max_length=255)


    # Имя - не является обязательным
    first_name = models.CharField(max_length=40, blank=True)
    # Фамилия - также не обязательна
    last_name = models.CharField(max_length=40, blank=True)
    # Наименование компании - не обязательна для физ лиц
    company_name = models.CharField(max_length=100, blank=True)

    # слоган или статус - куда же без него. Наследство от соц. сетей
    tagline = models.CharField(max_length=140, blank=True)

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

    user_photo = models.FileField(upload_to='/profile/', blank=False, default='/profile/defaultprofileimage.jpg')

    objects = AccountManager()

    # Имя пользователя мы будем выводить в нескольких местах.
    #  Так как это поле необязательно, мы включаем его в список REQUIRED_FIELDS.
    #  Обычно достаточно указать required=True, но так как мы заменяем модель User,
    #  Джанго требует явно определить это поле.
    # логинимся по email
    USERNAME_FIELD = 'email'
    # обязательное поле
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_user_photo(self):
        return self.user_photo
