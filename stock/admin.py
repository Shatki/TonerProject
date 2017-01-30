from django.contrib import admin
from .models import Item, Package


class ItemAdmin(admin.ModelAdmin):
    list_display = ('product',
                    'serial_number',
                    'package',
                    'country',
                    'warranty',
                    'quantity',
                    'measure',
                    )
    search_fields = ('serial_number', 'product',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if request.method not in ('GET', 'HEAD'):
                return False
        return super(ItemAdmin, self).has_change_permission(request, obj)


# Register your models here.
admin.site.register(Item, ItemAdmin)
admin.site.register(Package)
