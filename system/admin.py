from django.contrib import admin
from .models import Status, Order, Developer, Brand, Toner, Printer, Cartridge

admin.site.register(Toner)
admin.site.register(Printer)
admin.site.register(Cartridge)
admin.site.register(Status)
admin.site.register(Developer)
admin.site.register(Brand)
admin.site.register(Order)
