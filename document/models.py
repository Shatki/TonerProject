from django.db import models
from authentication.models import Account
from authentication.middleware import *
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from business.models import Cost, Tax
from contractor.models import Contractor
from system.models import Product, Measure, Country
from TonerProject.constants import date_minimal, date_maximal


# Приложение для формирования, хранения и обработки документации
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

    # Общие для всех документов поля
    delete = models.BooleanField(verbose_name=u'Черновик/Подлежит удалению', default=True)
    enable = models.BooleanField(verbose_name=u'действующий документ', default=False)
    created = models.DateTimeField(verbose_name=u'время/дата создания документа')
    creator = models.ForeignKey(Account, verbose_name=u'автор документа', related_name='contract_creator')
    modified = models.DateTimeField(verbose_name=u'время/дата изменения документа')
    modificator = models.ForeignKey(Account, verbose_name=u'изменил документ', related_name='contract_modificator')

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return 'Контракт № ' + self.number + ' от ' + str(self.date_begin)


# Consignment
# Накладная - это документ, используемый при передаче товарно-материальных ценностей от одного лица другому
# Накладная - это документ бухгалтерского учета, создание которого позволяет оформить операции
#               по отпуску и приему товарно-материальных ценностей (ТМЦ).
class Consignment(models.Model):
    class Meta:
        verbose_name = 'реализация'
        verbose_name_plural = 'реализации'
        db_table = 'consignment'

    number = models.CharField(max_length=10, verbose_name=u'номер накладной')
    date = models.DateField(verbose_name=u'дата документа')
    emitter = models.ForeignKey(Contractor, verbose_name=u'организация отпускающая груз',
                                related_name='consignment_emitter', default=None, null=True)
    receiver = models.ForeignKey(Contractor, verbose_name=u'организация принимающая груз',
                                 related_name='consignment_receiver', default=None, null=True)
    contract = models.ForeignKey(Contract, verbose_name=u'контракт',
                                 related_name='consignment_contract', default=None, null=True)

    items = models.ManyToManyField(Product, verbose_name=u'перемещаемый товар',
                                   through='ConsignmentTable',
                                   through_fields=('consignment', 'item'),
                                   related_name='consignment_items'
                                   )
    # Общие для всех документов поля
    delete = models.BooleanField(verbose_name=u'Черновик/Подлежит удалению', default=True)
    enable = models.BooleanField(verbose_name=u'действующий документ', default=False)
    created = models.DateTimeField(verbose_name=u'время/дата создания документа')
    creator = models.ForeignKey(Account, verbose_name=u'автор документа', related_name='consignment_creator')
    modified = models.DateTimeField(verbose_name=u'время/дата изменения документа')
    modificator = models.ForeignKey(Account, verbose_name=u'изменил документ', related_name='consignment_modificator')

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Consignment, self).save(*args, **kwargs)

    def __str__(self):
        return 'Накладная № ' + self.str_number() + ' от ' + self.str_date()

    def str_date(self):
        return str(self.date.day) + '/' + str(self.date.month) + '/' + str(self.date.year)

    def str_number(self):
        # Потом доработать для случаем сложных нумераций
        if self.number:
            return ('000000000' + str(int(self.number)))[-10:]
        else:
            return 'Новая'


class ConsignmentTable(models.Model):
    class Meta:
        verbose_name = 'продукт в накладной'
        verbose_name_plural = 'продукты в накладной'
        db_table = 'consignment_items'

    consignment = models.ForeignKey(Consignment, verbose_name=u'накладная')
    number = models.IntegerField(verbose_name=u'номер в накладной')
    item = models.ForeignKey(Product, verbose_name=u'продукт')
    country = models.ForeignKey(Country, verbose_name=u'страна происхождения', default=None, null=True)
    quantity = models.FloatField(verbose_name=u'количество')
    measure = models.ForeignKey(Measure, verbose_name=u'единица измерения', default=1)
    cost = models.FloatField(verbose_name=u'стоимость единицы продукта без налогов', default=0.0, null=True)
    tax = models.ForeignKey(Tax, verbose_name=u'налоговая ставка', default=None, null=True)

    def __str__(self):
        return self.item.category.name
