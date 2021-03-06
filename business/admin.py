from django.contrib import admin, messages
from .models import Status, Cost, Tax


class CostAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'value',
        'currency',
        'date',
        'time',
    )

    ordering = ('product', 'currency')
    search_fields = ('date', 'time',)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if request.method not in ('GET', 'HEAD'):
                return False
        return super(CostAdmin, self).has_change_permission(request, obj)


# Register your models here.
admin.site.register(Status)
admin.site.register(Tax)
admin.site.register(Cost, CostAdmin)
