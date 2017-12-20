from django.db import models
from TonerProject.validators import hexnumeric
from TonerProject.constants import date_minimal
from system.models import Product, Currency


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

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=u'товар', blank=False, null=False)
    value = models.FloatField(verbose_name=u'стоимость', default=1, blank=False, null=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name=u'валюта', blank=False, null=False)
    date = models.DateField(verbose_name=u'дата установки цены', default=date_minimal, blank=False, null=False)
    time = models.TimeField(verbose_name=u'время установки цены', blank=False, null=False)

    def __str__(self):
        return str(self.value)


class Tax(models.Model):
    class Meta:
        verbose_name = 'налог'
        verbose_name_plural = 'налоги'
        db_table = 'tax'

    name = models.CharField(max_length=30, default='без налога', verbose_name=u'вид налога', blank=False, null=False)
    value = models.FloatField(verbose_name=u'налоговая ставка', default=0, blank=False, null=False)
