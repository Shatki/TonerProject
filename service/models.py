from django.db import models
from authentication.models import Account
from system.models import Product
from TonerProject.validators import hexnumeric, numeric, validator_numerator, validator_warranty


# Create your models here.
class Status(models.Model):
    class Meta:
        verbose_name = 'статус'
        verbose_name_plural = 'статусы'
        db_table = 'status'

    name = models.CharField(max_length=20, verbose_name=u'статус заказа')
    color = models.CharField(max_length=6, validators=[hexnumeric], verbose_name=u'цвет пиктограммы', default='ffffff')

    def __str__(self):
        return self.name

    @property
    def csscolor(self):
        return '#%s' % self.color


class Work(models.Model):
    class Meta:
        verbose_name = 'вид работы'
        verbose_name_plural = 'виды работ'
        db_table = 'work'

    name = models.CharField(verbose_name=u'вид работы', max_length=30, blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        db_table = 'order'

    number = models.CharField(max_length=10, verbose_name=u'номер заказа', validators=[validator_numerator],
                              help_text=u"пожалуйста используйте следующий формат: AA-xxxxxxx")
    date = models.DateField(verbose_name=u'дата заказа', auto_now_add=True)
    user = models.ForeignKey(Account, verbose_name=u'клиент')
    work = models.ForeignKey(Work, verbose_name=u'вид работ', default=None)
    cost = models.IntegerField(verbose_name=u'стоимость', editable=True, default=0)
    # Оборудованиe
    product = models.ForeignKey(Product, verbose_name=u'устройство', default=None)
    # cartridge = models.ForeignKey(Cartridge, verbose_name=u'Картридж')
    # Вид работы
    comments = models.TextField(max_length=100, verbose_name=u'комментарий', blank=True)
    status = models.ForeignKey(Status, verbose_name=u'статус заказа', on_delete=None)

    def __str__(self):
        return self.number


"""
class Brand(models.Model):
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        db_table = 'brand'

    name = models.CharField(verbose_name=u'Бренд', max_length=20,
                            help_text=u"Бренд это промышленый стандарт или тип производимого товара")

    def __str__(self):
        return self.name

# модели на заправку картриджей
class Toner(models.Model):
    class Meta:
        verbose_name = 'Тонер'
        verbose_name_plural = 'Тонеры'
        db_table = 'toner'
    name = models.CharField(verbose_name=u'Тонер', max_length=20)
    brand = models.ForeignKey(Brand, verbose_name=u'Марка тонера', unique=False)
    developer = models.ForeignKey(Developer, verbose_name=u'Производитель тонера', unique=False)
    def __str__(self):
        return "%s %s" % (self.brand.name, self.name)


class Cartridge(models.Model):
    class Meta:
        verbose_name = 'Картридж'
        verbose_name_plural = 'Картриджи'
        db_table = 'cartridge'

    name = models.CharField(verbose_name=u'Модель картриджа', max_length=20, blank=False)
    toner = models.ForeignKey(Toner, verbose_name=u'Тип тонера', blank=False)
    weight = models.IntegerField(verbose_name=u'Вес(грамм)', default=50)
    resource = models.IntegerField(verbose_name=u'Ресурс печати одной заправки(страниц)', default=1000)
    refill_price = models.IntegerField(verbose_name=u'Стоимость заправки(рублей)', default=400)
    def __str__(self):
        return self.name


class Printer(models.Model):
    class Meta:
        verbose_name = 'Печатающее устройство'
        verbose_name_plural = 'Печатающие устройства'
        db_table = 'printer'
    name = models.CharField(verbose_name=u'Модель принтера', max_length=20)
    developer = models.ForeignKey(Developer, verbose_name=u'Производитель оборудования')
    cartridge = models.ForeignKey(Cartridge, verbose_name=u'Тип используемого картриджа')
    def __str__(self):
        return self.name


class RepairPart(models.Model):
    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты и ЗЧ'
        db_table = 'repair part'

    name = models.CharField(verbose_name=u'Компонент', max_length=20)
    cartridge = models.ForeignKey(Cartridge, blank=True, verbose_name=u'Используется в картридже')
    printer = models.ForeignKey(Printer, blank=True, verbose_name=u'Используется в устройстве')

    def __str__(self):
        return self.name


class Device(models.Model):
    class Meta:
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'
        db_table = 'device'

    name = models.CharField(verbose_name=u'Модель устройства', max_length=20)
    brand = models.ForeignKey(Brand, verbose_name=u'Производитель устройства')

    def __str__(self):
        return "%s %s" % (self.brand.name, self.name)

"""
