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
    seller = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name=u'продавец',
                               related_name='contract_seller')
    buyer = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name=u'покупатель',
                              related_name='contract_buyer')
    date_begin = models.DateField(verbose_name=u'дата заключения контракта', default=date_minimal)
    date_expire = models.DateField(verbose_name=u'дата истечения контракта', default=date_maximal)

    # Общие для всех документов поля
    delete = models.BooleanField(verbose_name=u'черновик/подлежит удалению', default=True)
    enable = models.BooleanField(verbose_name=u'действующий документ', default=False)
    created = models.DateTimeField(verbose_name=u'время/дата создания документа')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=u'автор документа',
                                related_name='contract_creator')
    modified = models.DateTimeField(verbose_name=u'время/дата изменения документа')
    modificator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=u'изменил документ',
                                    related_name='contract_modificator')

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return 'Контракт № %s от %s' % (self.number, str(self.date_begin))

# DocType
class DocType(models.Model):
    class Meta:
        verbose_name = 'тип документа'
        verbose_name_plural = 'типы документов'
        db_table = 'doctype'

    name = models.CharField(max_length=30, verbose_name=u'название документа (например, Накладная)')
    action = models.CharField(max_length=30, verbose_name=u'название документа (например, Реализация)')
    type = models.CharField(max_length=30, verbose_name=u'тип документа (например, Consignment)')

    def __str__(self):
        return self.name


# Document
# Накладная - это документ, используемый при передаче товарно-материальных ценностей от одного лица другому
# Накладная - это документ бухгалтерского учета, создание которого позволяет оформить операции
#               по отпуску и приему товарно-материальных ценностей (ТМЦ).
class Document(models.Model):
    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'
        db_table = 'document'

    type = models.ForeignKey(DocType, verbose_name=u'продукция',
                             related_name='document_items', on_delete=models.CASCADE)
    number = models.CharField(max_length=10, verbose_name=u'номер документа')
    date = models.DateField(verbose_name=u'дата документа')
    emitter = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name=u'организация эмитент',
                                related_name='document_emitter', default=None, null=True)
    receiver = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name=u'организация контрагент',
                                 related_name='document_receiver', default=None, null=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name=u'контракт',
                                 related_name='document_contract', default=None, null=True)

    items = models.ManyToManyField(Product, verbose_name=u'продукция в документе',
                                   through='DocumentTable',
                                   through_fields=('document', 'item'),
                                   related_name='document_items'
                                   )
    # Общие для всех документов поля
    delete = models.BooleanField(verbose_name=u'черновик/подлежит удалению', default=True)
    enable = models.BooleanField(verbose_name=u'действующий документ', default=False)
    created = models.DateTimeField(verbose_name=u'время/дата создания документа')
    creator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=u'автор документа',
                                related_name='document_creator')
    modified = models.DateTimeField(verbose_name=u'время/дата изменения документа')
    modificator = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name=u'изменил документ',
                                    related_name='document_modificator')

    def save(self, *args, **kwargs):
        # On save, update timestamps
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(Document, self).save(*args, **kwargs)

    def __str__(self):
        return '%s № %s от %s' % (self.type.name, self.str_number(), self.str_date())

    def str_date(self):
        return '%s/%s/%s' % (str(self.date.day), str(self.date.month),str(self.date.year))

    def str_number(self):
        # Потом доработать для случаем сложных нумераций
        if self.number:
            return ('000000000' + str(int(self.number)))[-10:]
        else:
            return 'Новый документ'


class DocumentTable(models.Model):
    class Meta:
        verbose_name = 'продукт в документе'
        verbose_name_plural = 'продукция в документе'
        db_table = 'document_items'

    document = models.ForeignKey(Document, on_delete=models.CASCADE, verbose_name=u'документ')
    number = models.IntegerField(verbose_name=u'номер в документе')
    item = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=u'продукт')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name=u'страна происхождения', default=None,
                                null=True)
    quantity = models.FloatField(verbose_name=u'количество', default=0.00)
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, verbose_name=u'единица измерения', default=1)
    cost = models.FloatField(verbose_name=u'стоимость единицы продукта без налогов', default=0.00, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE, verbose_name=u'налоговая ставка', default=None, null=True)

    def __str__(self):
        return self.item.category.name
