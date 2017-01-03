from django.contrib import admin
from .models import Status, Item, Package

# Register your models here.
admin.site.register(Status)
admin.site.register(Item)
admin.site.register(Package)
