from django.db import models
from contractor.models import Contractor
from trade.models import Item
from .constants import date_minimal, date_maximal


# Приложение для формирования, хранения и обработки документации


# Consignment
# Накладная - это документ, используемый при передаче товарно-материальных ценностей от одного лица другому
# Накладная - это документ бухгалтерского учета, создание которого позволяет оформить операции
#               по отпуску и приему товарно-материальных ценностей (ТМЦ).
class Consignment(models.Model):
    class Meta:
        verbose_name = 'накладная'
        verbose_name_plural = 'накладные'
        db_table = 'consignment'

    number = models.CharField(max_length=20, verbose_name=u'номер накладной')
    date = models.DateField(verbose_name=u'дата документа')
    emitter = models.ForeignKey(Contractor, verbose_name=u'организация отпускающая груз',
                                related_name='consignment_emitter')
    receiver = models.ForeignKey(Contractor, verbose_name=u'организация принимающая груз',
                                 related_name='consignment_receiver')
    items = models.ManyToManyField(Item, verbose_name=u'перемещаемый товар')
    status = models.BooleanField(verbose_name=u'статус проведения', default=False)

    def __str__(self):
        return '№ ' + self.number + ' от ' + str(self.date)


class Contract(models.Model):
    class Meta:
        verbose_name = 'контракт'
        verbose_name_plural = 'контракты'
        db_table = 'contract'

    number = models.CharField(max_length=20, verbose_name=u'номер контракта')
    seller = models.ForeignKey(Contractor, verbose_name=u'продавец',
                               related_name='contract_seller')
    buyer = models.ForeignKey(Contractor, verbose_name=u'покупатель',
                              related_name='contract_buyer')
    date_begin = models.DateField(verbose_name=u'дата заключения контракта', default=date_minimal)
    date_expire = models.DateField(verbose_name=u'дата истечения контракта', default=date_maximal)

    def __str__(self):
        return '№ ' + self.number + ' от ' + str(self.date_begin)
