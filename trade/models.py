from django.db import models
from system.models import Product, Country
from TonerProject.validators import hexnumeric, numeric, validator_numerator, validator_warranty


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
    # Класс товаров для индивидуального учета по серийным номерам
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        db_table = 'item'

    product = models.ForeignKey(Product, verbose_name=u'продукт', default=None)
    serial_number = models.CharField(max_length=30, verbose_name=u'серийный номер продукта', default='0000000000')
    country = models.ForeignKey(Country, verbose_name=u'страна производитель', default=None)
    warranty = models.IntegerField(default=6, verbose_name=u'гарантийный срок', validators=[validator_warranty])
    package = models.ForeignKey(Package, verbose_name=u'тип поставки', null=True)

    def __str__(self):
        return self.product.__str__()
