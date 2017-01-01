from django.db import models
from TonerProject.validators import hexnumeric, numeric, validator_numerator

# ********** Основные Классы *************
class Code(models.Model):
    class Meta:
        verbose_name = 'код товара'
        verbose_name_plural = 'коды товаров'

    code = models.CharField(verbose_name=u'код товара', max_length=10, unique=True,
                            help_text=u"уникальный код товара служащий идентификатором товара в системе")

    code_ean13 = models.CharField(max_length=13, verbose_name='штрих код EAN-13', default=None,
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
class Country(models.Model):
    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        db_table = 'country'

    name = models.CharField(max_length=30, verbose_name=u'наименование страны')

    def __str__(self):
        return self.name


class Developer(models.Model):
    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'
        db_table = 'developer'

    name = models.CharField(verbose_name=u'производитель товара', max_length=20)

    site = models.CharField(verbose_name=u'web сайт компании', max_length=30, unique=True, null=True, default=None)

    def __str__(self):
        return self.name

    def website(self):
        return self.site


class Category(models.Model):
    class Meta:
        verbose_name = 'категория товара'
        verbose_name_plural = 'категории товаров'
        db_table = 'category'

    name = models.CharField(verbose_name=u'категория товара', max_length=30,
                            help_text=u"наименование категории товара")
    parent = models.ForeignKey("self", verbose_name=u'Родительскиая категория', null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Type(models.Model):
    class Meta:
        verbose_name = 'группа характеристик'
        verbose_name_plural = 'группы характеристик'
        db_table = 'type_of_feature'

    name = models.CharField(verbose_name=u'группа характеристики', max_length=40,
                            help_text=u"наименование группы характеристики товара")
    belongs = models.ManyToManyField(Category, verbose_name=u'принадлежность к категории товаров:')

    def __str__(self):
        return self.belongs.first().name + " | " + self.name


class Feature(models.Model):
    class Meta:
        verbose_name = 'характеристика'
        verbose_name_plural = 'характиристики'
        db_table = 'feature'

    name = models.CharField(verbose_name=u'характеристика', max_length=70,
                            help_text=u"характеристика товара", unique=True)

    def __str__(self):
        return self.name


class Features(models.Model):
    class Meta:
        verbose_name = 'характиристика товара'
        verbose_name_plural = 'характиристики товаров'
        db_table = 'features'

    feature = models.ForeignKey(Feature, verbose_name=u'наименование характеристики:')
    group = models.ForeignKey(Type, verbose_name=u'группа характеристик товара',
                              help_text=u"группа принадлежности характеристики")
    name = models.CharField(verbose_name=u'Модель или количество', max_length=70,
                            help_text=u"описание характеристик товара, "
                                      u"может иметь количественное или булево значение 'есть/нет'")
    def __str__(self):
        return self.group.belongs.first().name + ' | ' + self.group.name + ' | ' \
               + self.feature.name + ': ' + self.name


class Product(models.Model):
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        db_table = 'product'

    name = models.CharField(verbose_name=u'наименование продукта', max_length=30,
                            help_text=u"наименование продукта")
    category = models.ForeignKey(Category, verbose_name=u'категория продукта')
    developer = models.ForeignKey(Developer, verbose_name=u'производитель продукта')
    code = models.ForeignKey(Code, verbose_name=u'коды продукта:', null=True, blank=True)
    features = models.ManyToManyField(Features, verbose_name=u'характеристики продукта', blank=True)
    include = models.ManyToManyField("self", symmetrical=True, default=None, verbose_name=u'подходит для:', blank=True)

    def __str__(self):
        return self.category.name + ' ' + self.developer.name + ' ' + self.name

