from django.db import models
from authentication.models import Account
from .validators import hexnumeric, numeric, validator_numerator


class Status(models.Model):
    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        db_table = 'status'

    name = models.CharField(max_length=20, verbose_name=u'Статус заказа')
    color = models.CharField(max_length=6, validators=[hexnumeric], verbose_name=u'Цвет пиктограммы', default='ffffff')

    def __str__(self):
        return self.name

    @property
    def csscolor(self):
        return '#%s' % self.color


# ********** Основные Классы *************
class Code(models.Model):
    class Meta:
        verbose_name = 'Код товара'
        verbose_name_plural = 'Коды товаров'

    code = models.CharField(verbose_name=u'Код товара', max_length=10, unique=True,
                            help_text=u"Уникальный код товара служащий идентификатором товара в системе")

    code_ean13 = models.CharField(max_length=13, verbose_name='Штрих код EAN-13', default=None,
                                  validators=[numeric])

    # objects = models.Manager()
    # В последствии тут будут дополнены поля
    # Application constants
    CODE_DESCRIPTOR = 'SH-'
    """
    def get_code(self):
        try:
            codes = Code.objects.all()
            for i in range(1, 99):
                code = self.format_code(i)
                # print(code)
                if code not in codes:
                    return code
        except:
            return self.format_code(1)

    def format_code(self, num):
        code = self.CODE_DESCRIPTOR + ('0000000' + str(num))[-8:]
        return code
    """

    def __str__(self):
        return self.code

    def ean13(self):
        return self.code_ean13


# *********** Общие Классы **************
class Developer(models.Model):
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        db_table = 'developer'

    name = models.CharField(verbose_name=u'Производитель товара', max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'
        db_table = 'category'

    name = models.CharField(verbose_name=u'Категория товара', max_length=30,
                            help_text=u"Наименование категории товара")

    def __str__(self):
        return self.name


class Type(models.Model):
    class Meta:
        verbose_name = 'Группа характеристик'
        verbose_name_plural = 'Группы характеристик'
        db_table = 'type_of_feature'

    name = models.CharField(verbose_name=u'Группа характеристики', max_length=40,
                            help_text=u"Наименование группы характеристики товара")
    belongs = models.ManyToManyField(Category, verbose_name=u'Принадлежность к категории товаров:')

    def __str__(self):
        return self.name


class Feature(models.Model):
    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характиристики'
        db_table = 'feature'

    name = models.CharField(verbose_name=u'Характеристика', max_length=70,
                            help_text=u"Характеристика товара")

    def __str__(self):
        return self.name


class Features(models.Model):
    class Meta:
        verbose_name = 'Характиристика товара'
        verbose_name_plural = 'Характиристики товара'
        db_table = 'features'

    name = models.CharField(verbose_name=u'Описание', max_length=70,
                            help_text=u"Описание характеристик товара")
    group = models.ForeignKey(Type, verbose_name=u'Группа характеристик товара',
                              help_text=u"Группа принадлежности характеристики")
    feature = models.ForeignKey(Feature, verbose_name=u'Наименование характеристики:')

    def __str__(self):
        return self.group.belongs.first().name + ' | ' + self.feature.name + ':' + self.name


class Item(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        db_table = 'item'

    name = models.CharField(verbose_name=u'Наименование товара', max_length=30,
                            help_text=u"Наименование товара")
    category = models.ForeignKey(Category, verbose_name=u'Категория товара')
    developer = models.ForeignKey(Developer, verbose_name=u'Производитель товара')
    code = models.ForeignKey(Code, verbose_name=u'Коды товара:', null=True, blank=True)
    features = models.ManyToManyField(Features, verbose_name=u'Характеристики товара', blank=True)
    include = models.ManyToManyField("self", default=None, verbose_name=u'Подходит для:', blank=True)

    def __str__(self):
        return self.category.name + ' ' + self.developer.name + ' ' + self.name


class Work(models.Model):
    class Meta:
        verbose_name = 'Вид работы'
        verbose_name_plural = 'Вид работ'
        db_table = 'work'

    name = models.CharField(verbose_name=u'Вид работы', max_length=30, blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order'

    number = models.CharField(max_length=10, verbose_name=u'Номер заказа', validators=[validator_numerator],
                              help_text=u"Пожалуйста используйте следующий формат: AA-xxxxxxx")
    date = models.DateField(verbose_name=u'Дата заказа', auto_now_add=True)
    user = models.ForeignKey(Account, verbose_name=u'Клиент')
    work = models.ForeignKey(Work, verbose_name=u'Вид работ', default=None)
    cost = models.IntegerField(verbose_name=u'Стоимость', editable=True, default=0)
    # Оборудованиe
    item = models.ForeignKey(Item, verbose_name=u'Устройство', default=None)
    # cartridge = models.ForeignKey(Cartridge, verbose_name=u'Картридж')
    # Вид работы
    comments = models.TextField(max_length=100, verbose_name=u'Комментарий', blank=True)
    status = models.ForeignKey(Status, verbose_name=u'Статус заказа', on_delete=None)

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
