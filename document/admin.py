from django.contrib import admin
from .models import DocType, Document, Contract, DocumentTable

class DocTypeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'type')


class DocumentTableInline(admin.TabularInline):
    model = DocumentTable
    extra = 1


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'number',
                    '__str__',
                    'emitter',
                    'receiver',
                    'enable',
                    'delete',
                    'created',
                    'creator',
                    'modified',
                    'modificator',
                    )

    search_fields = ('number', 'date', 'creator')
    ordering = ('id',)
    inlines = (DocumentTableInline,)


class DocumentTableAdmin(admin.ModelAdmin):
    inlines = (DocumentTableInline,)


class ContractAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'number',
                    '__str__',
                    'buyer',
                    'seller',
                    'enable',
                    'delete',
                    'created',
                    'creator',
                    'modified',
                    'modificator',
                    )

    search_fields = ('number', 'buyer', 'seller',)
    ordering = ('id',)


# Register your models here.
admin.site.register(DocType)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Contract, ContractAdmin)
