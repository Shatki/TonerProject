from django import forms
from django.contrib import admin
from .models import Contractor, Type

"""
class BankChangeForm(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ('name',
                  'address',
                  'account',
                  'bik',)
"""


# Register your models here.
@admin.register(Contractor)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'boss_first_name',
                    'boss_second_name',
                    'boss_last_name',
                    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'type',
            )}),
        (u'Контактная информация', {
            'fields': (
                'boss_first_name',
                'boss_second_name',
                'boss_last_name',
                'address',
                'phone',
            )}),
        (u'Реквизиты', {
            'fields': (
                'inn',
                'ogrn',
                'okpo',
                'okato',
                'bank',
                'account',
            )}),
    )

    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Type)
