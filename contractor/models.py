from django.db import models
from TonerProject.validators import numeric, phone
from .constants import PERSON, COMPANY, BANK, GOV_BANK, GOV_COMPANY


# Create your models here.
class Type(models.Model):
    class Meta:
        verbose_name = 'вид контрагента'
        verbose_name_plural = 'виды контрагентов'
        db_table = 'contractor_type'

    CONTRACTOR_CHOICES = (
        (PERSON, 'Физическое лицо'),
        (COMPANY, 'Коммерческая организация'),
        (BANK, 'Банк'),
        (GOV_BANK, 'Центральный банк'),
        (GOV_COMPANY, 'Государственная учреждение'),
    )

    name = models.CharField(verbose_name=u'вид контрагента', unique=True, default=PERSON,
                            max_length=100, blank=False, choices=CONTRACTOR_CHOICES)

    def __str__(self):
        return self.name

    def type_person(self):
        return self.PERSON

    def type_bank(self):
        return self.bank


class Contractor(models.Model):
    # Контрагент
    # Наименование компании - не обязательна для физ лиц
    class Meta:
        verbose_name = 'контрагент'
        verbose_name_plural = 'контрагенты'
        db_table = 'contractor'
        # ordering = ('name',)

    name = models.CharField(verbose_name=u'наименование компании', max_length=100)
    boss_first_name = models.CharField(verbose_name=u'имя руководителя', max_length=40, blank=True, null=True)  # Имя
    boss_second_name = models.CharField(verbose_name=u'отчество руководителя', max_length=40, blank=True,
                                        null=True)  # Отчество
    boss_last_name = models.CharField(verbose_name=u'фамилия руководителя', max_length=40, blank=True,
                                      null=True)  # Фамилия
    phone = models.CharField(verbose_name=u'контактный телефон', max_length=10, validators=[phone],
                             null=True, blank=True)
    inn = models.CharField(verbose_name=u'ИНН', unique=True, max_length=12, validators=[numeric],
                           null=True, blank=True)  # ИНН
    ogrn = models.CharField(verbose_name=u'ОГРН', unique=True, max_length=15, validators=[numeric],
                            null=True, blank=True)  # ОГРН
    okpo = models.CharField(verbose_name=u'ОКПО', max_length=9, validators=[numeric], null=True, blank=True)  # ОКПО
    okato = models.CharField(verbose_name=u'ОКАТО', max_length=11, validators=[numeric], null=True, blank=True)  # ОКАТО
    address = models.CharField(verbose_name=u'адрес организации', max_length=100, null=True, blank=True)

    bank = models.ForeignKey('self', verbose_name=u'банк', blank=True, null=True)
    account = models.CharField(verbose_name=u'банковский счёт', max_length=20,
                               validators=[numeric], null=True, blank=True)  # счет
    type = models.ForeignKey(Type, verbose_name=u'вид контрагента', null=True, blank=True)
    bik = models.CharField(verbose_name=u'БИК', unique=True, max_length=9, db_index=True,
                           validators=[numeric], blank=True, null=True)  # БИК атрибут банков

    def __str__(self):
        return self.name

    def get_boss_full_name(self):
        return ' '.join([self.boss_first_name, self.boss_second_name, self.boss_last_name])

    def get_boss_short_name(self):
        return ' '.join([self.boss_first_name, self.boss_second_name])
