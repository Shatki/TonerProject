from django.db import models
from system.models import Product, Country, Measure
from TonerProject.validators import validator_warranty


# Create your models here.

class Package(models.Model):
    class Meta:
        verbose_name = 'тип поставки'
        verbose_name_plural = 'типов поставок'
        db_table = 'package'

    name = models.CharField(max_length=10, verbose_name=u'название типа поставки')

    def __str__(self):
        return self.name


class Item(models.Model):
    # реальный товар
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        db_table = 'item'

    # main fields
    product = models.ForeignKey(Product, verbose_name=u'продукт', default=None)
    country = models.ForeignKey(Country, verbose_name=u'страна производитель', default=None)
    warranty = models.IntegerField(default=6, verbose_name=u'гарантийный срок', validators=[validator_warranty])
    package = models.ForeignKey(Package, verbose_name=u'тип поставки', null=True)

    # addition fields
    serial_number = models.CharField(max_length=30, verbose_name=u'серийный номер продукта',
                                     default=None, null=True, blank=True)
    quantity = models.FloatField(verbose_name=u'Количество', default=1)
    measure = models.ForeignKey(Measure, verbose_name=u'Единица измерения', default=1)

    def __str__(self):
        return str(self.product) + ', ' + self.package.name + ' [' + self.serial_number + ']'
