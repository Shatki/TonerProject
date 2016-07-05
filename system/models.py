from django.db import models
from authentication.models import Account
from django.core.validators import RegexValidator, ValidationError


def validator_numerator(value):
    a = value[0:2]  # Первые две буквы
    n = value[3:10]  # Последние 7 цифр
    if value[2] != '-':
        raise ValidationError(u'%s не корректный номер заказа' % value)
    if not (a.isalpha() & a.isupper()):
        raise ValidationError(u'%s укажите первые две заглавные буквы кода' % value)
    if not n.isdigit():
        raise ValidationError(u'%s укажите цифровой номер заказа' % value)


class Status(models.Model):
    class Meta:
        db_table = 'status'

    hexnumeric = RegexValidator(r'^[0-9a-fA-F]*$', message=u'Цвет пиктограммы указывается в шестнадцатиричной системе.')
    name = models.CharField(max_length=20, verbose_name=u'Статус заказа')
    color = models.CharField(max_length=6, validators=[hexnumeric], verbose_name=u'Цвет пиктограммы', default='ffffff')

    def __str__(self):
        return self.name

    @property
    def csscolor(self):
        return '#' + self.csscolor


class Developer(models.Model):
    class Meta:
        db_table = 'developer'

    name = models.CharField(verbose_name=u'Производитель', max_length=20)

    def __str__(self):
        return self.name


class Brand(models.Model):
    class Meta:
        db_table = 'brand'

    name = models.CharField(verbose_name=u'Бренд', max_length=20)

    def __str__(self):
        return self.name


# модели на заправку картриджей
class Toner(models.Model):
    class Meta:
        db_table = 'toner'

    name = models.CharField(verbose_name=u'Тонер', max_length=20)
    brand = models.ForeignKey(Brand, verbose_name=u'Марка тонера')
    developer = models.ForeignKey(Developer, verbose_name=u'Производитель тонера')

    def __str__(self):
        return self.brand.name + " " + self.name


class Cartridge(models.Model):
    class Meta:
        db_table = 'cartridge'

    name = models.CharField(verbose_name=u'Модель картриджа', max_length=20)
    toner = models.ForeignKey(Toner, verbose_name=u'Тип тонера')
    weight = models.IntegerField(verbose_name=u'Вес(грамм)')

    def __str__(self):
        return self.name


class Printer(models.Model):
    class Meta:
        db_table = 'printer'

    name = models.CharField(verbose_name=u'Модель принтера', max_length=20)
    developer = models.ForeignKey(Developer, verbose_name=u'Производитель оборудования')
    cartridge = models.ForeignKey(Cartridge, verbose_name=u'Тип используемого картриджа')

    def __str__(self):
        return self.name


# Модель приемки заказов на картриджи.
class Order(models.Model):
    class Meta:
        db_table = 'order'

    number = models.CharField(max_length=10, verbose_name=u'Номер заказа', validators=[validator_numerator],
                              help_text=u"Пожалуйста используйте следующий формат: AA-xxxxxxx")
    date = models.DateField(verbose_name=u'Дата заказа')
    user = models.ForeignKey(Account, verbose_name=u'Клиент')
    cartridge = models.ForeignKey(Cartridge, verbose_name=u'Картридж')
    comments = models.TextField(max_length=100, verbose_name=u'Комментарий', blank=True)
    status = models.ForeignKey(Status, verbose_name=u'Статус заказа')

    def __str__(self):
        return self.number
