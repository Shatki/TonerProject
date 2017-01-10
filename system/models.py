from django.db import models
from TonerProject.validators import hexnumeric, numeric, validator_numerator, validator_path
from django.utils.text import slugify
from .translit_v5 import transliterate


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
        ordering = ('name',)

    name = models.CharField(verbose_name=u'категория товара', max_length=30,
                            help_text=u"наименование категории товара")
    path = models.CharField(verbose_name=u'наименование для адресной строки', max_length=30,
                            validators=[validator_path],
                            help_text=u"категории товара в адресной строке в латинских символах")
    parent = models.ForeignKey("self", verbose_name=u'Родительскиая категория', null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    def get_path(self):
        path = '/'
        if self.parent is not None:
            path = self.parent.get_path() + self.parent.path + '/'
        return path

    get_path.short_description = 'Путь'


class Type(models.Model):
    class Meta:
        verbose_name = 'группа характеристик'
        verbose_name_plural = 'группы характеристик'
        db_table = 'type_of_feature'
        ordering = ('id',)

    name = models.CharField(verbose_name=u'группа характеристики', max_length=40,
                            help_text=u"наименование группы характеристики товара")
    belongs = models.ManyToManyField(Category, verbose_name=u'принадлежность к категории товаров')

    def __str__(self):
        return self.belongs.first().name + " | " + self.name

    def belongs_list(self):
        belongs_str = ''
        belongs_list = self.belongs.all()
        for belongs in belongs_list:
            belongs_str += ', ' + belongs.name
        return belongs_str.lstrip(', ')

    belongs_list.short_description = 'Принадлежность к категориям'


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
        ordering = ('group',)

    feature = models.ForeignKey(Feature, verbose_name=u'наименование характеристики')
    group = models.ForeignKey(Type, verbose_name=u'группа характеристик товара',
                              help_text=u"группа принадлежности характеристики")
    name = models.CharField(verbose_name=u'Модель или количество', max_length=70,
                            help_text=u"описание характеристик товара, "
                                      u"может иметь количественное или булево значение 'есть/нет'")

    def __str__(self):
        return self.group.belongs.first().name + ' | ' + self.group.name + ' | ' \
               + self.feature.name + ': ' + self.name

    def only_name(self):
        return self.name


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
    features = models.ManyToManyField(Features, verbose_name=u'характеристики продукта',
                                      related_name='features', blank=True)
    include = models.ManyToManyField('self', symmetrical=True, default=None,
                                     verbose_name=u'подходит для:', blank=True)
    # Параметры для отображения информации в наименовании
    first_view = models.ForeignKey(Features, verbose_name=u'первая характеристика',
                                   related_name='first_features_view', null=True, blank=True)
    second_view = models.ForeignKey(Features, verbose_name=u'вторая характеристика',
                                    related_name='second_features_view', null=True, blank=True)

    third_view = models.ForeignKey(Features, verbose_name=u'третья характеристика',
                                   related_name='third_features_view', null=True, blank=True)

    fourth_view = models.ForeignKey(Features, verbose_name=u'четвертая характеристика',
                                    related_name='fourth_features_view', null=True, blank=True)

    fifth_view = models.ForeignKey(Features, verbose_name=u'пятая характеристика',
                                   related_name='fifth_features_view', null=True, blank=True)

    sixth_view = models.ForeignKey(Features, verbose_name=u'шестая характеристика',
                                   related_name='sixth_features_view', null=True, blank=True)

    def __str__(self):
        retstr = self.category.name + ' ' + self.developer.name + ' ' + self.name
        if self.first_view:
            retstr = retstr + ', ' + self.first_view.name

        if self.second_view:
            retstr = retstr + ', ' + self.second_view.name

        if self.third_view:
            retstr = retstr + ', ' + self.third_view.name

        if self.fourth_view:
            retstr = retstr + ', ' + self.fourth_view.name

        if self.fifth_view:
            retstr = retstr + ', ' + self.fifth_view.name

        if self.sixth_view:
            retstr = retstr + ', ' + self.sixth_view.name
        return retstr

    def __unicode__(self):
        retstr = self.category.name + ' ' + self.developer.name + ' ' + self.name
        if self.first_view:
            retstr = retstr + ', ' + self.first_view.name

        if self.second_view:
            retstr = retstr + ', ' + self.second_view.name

        if self.third_view:
            retstr = retstr + ', ' + self.third_view.name

        if self.fourth_view:
            retstr = retstr + ', ' + self.fourth_view.name

        if self.fifth_view:
            retstr = retstr + ', ' + self.fifth_view.name

        if self.sixth_view:
            retstr = retstr + ', ' + self.sixth_view.name
        return retstr
