from django.db import models
from TonerProject.validators import hexnumeric
from TonerProject.constants import date_minimal
from system.models import Product


# Create your models here.
class Status(models.Model):
    class Meta:
        verbose_name = 'статус заказа'
        verbose_name_plural = 'статусы заказов'
        db_table = 'trade_status'

    name = models.CharField(max_length=20, verbose_name=u'статус заказа')
    color = models.CharField(max_length=6, validators=[hexnumeric], verbose_name=u'цвет пиктограммы', default='ffffff')

    def __str__(self):
        return self.name

    @property
    def csscolor(self):
        return '#%s' % self.color


class Cost(models.Model):
    class Meta:
        verbose_name = 'цена'
        verbose_name_plural = 'цены'
        db_table = 'cost'

    product = models.ForeignKey(Product, verbose_name=u'Товар', blank=False, null=False)
    value = models.FloatField(verbose_name=u'стоимость', default=1, blank=False, null=False)
    date = models.DateField(verbose_name=u'дата установки цены', default=date_minimal, blank=False, null=False)
    time = models.TimeField(verbose_name=u'время установки цены', blank=False, null=False)

    def __str__(self):
        return str(self.value)
