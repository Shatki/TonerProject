from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

class Account(AbstractBaseUser):
    #Авторизация будет происходить по E-mail
    email = models.EmailField(unique=True)
    # username нам  необходим для отображении записей и страницы действий
    username = models.CharField(max_length=40, unique=True)

    # Имя - не является обязательным
    first_name = models.CharField(max_length=40, blank=True)
    # Фамилия - также не обязательна
    last_name = models.CharField(max_length=40, blank=True)

    # слоган или статус - куда же без него. Наследство от соц. сетей
    tagline = models.CharField(max_length=140, blank=True)

    # Атрибут суперпользователя
    is_admin = models.BooleanField(default=False)

    # Сохраняем время создания и обновления аккаунта пользователя.
    # Устанавливая auto_now_add=True, мы говорим Джанго автоматически
    # ставить время при создании, причем далее поле будет нередактируемым.
    #  Аналогично и auto_now=True, разница в том, что поле каждый раз обновляется с обновлением объекта
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    # Имя пользователя мы будем выводить в нескольких местах.
    #  Так как это поле необязательно, мы включаем его в список REQUIRED_FIELDS.
    #  Обычно достаточно указать required=True, но так как мы заменяем модель User,
    #  Джанго требует явно определить это поле.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name
