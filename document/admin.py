from django.contrib import admin
from .models import Consignment, Contract, ConsignmentTable


class ConsignmentTableInline(admin.TabularInline):
    model = ConsignmentTable
    extra = 1


class ConsignmentAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'emitter',
                    'receiver',
                    'status',
                    )

    search_fields = ('number', 'date')
    ordering = ('id',)
    inlines = (ConsignmentTableInline,)


class ConsignmentTableAdmin(admin.ModelAdmin):
    inlines = (ConsignmentTableInline,)


class ContractAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'buyer',
                    'seller',
                    )

    search_fields = ('number', 'buyer', 'seller',)
    ordering = ('id',)


# Register your models here.
admin.site.register(Consignment, ConsignmentAdmin)
admin.site.register(Contract, ContractAdmin)
