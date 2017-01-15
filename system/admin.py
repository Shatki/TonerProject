from django.contrib import admin
from .models import Code, Country, Developer, Type, Feature, Features, Category, Product, Currency, Course


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',
                    )

    search_fields = ('name',)
    ordering = ('name',)


class DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'site',
                    )

    search_fields = ('name',)
    ordering = ('name',)


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',
                    )

    search_fields = ('name',)
    ordering = ('name',)


class FeaturesAdmin(admin.ModelAdmin):
    list_display = ('group',
                    'feature',
                    'name',
                    )

    # search_fields = ('name',)
    ordering = ('group',)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'belongs_list',
                    )

    search_fields = ('name',)
    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'parent',
                    'get_path',
                    )
    search_fields = ('name',)
    ordering = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__',
                    'code',
                    'category',
                    'developer',
                    )
    fieldsets = (
        (None, {
            'fields': (
                'name',
                'category',
                'developer',
                'code',
            )}),
        (u'Технические характеристики', {
            'fields': (
                'features',
                'include',
            )}),
        (u'Настройка полей отображения характеристик в наименовании', {
            'fields': (
                'first_view',
                'second_view',
                'third_view',
                'fourth_view',
                'fifth_view',
                'sixth_view',
            )}),
    )

    search_fields = ('name',)
    ordering = ('developer',)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'name_4217',
                    'code_4217',
                    #                    'course',
                    )
    search_fields = ('name',)
    ordering = ('id',)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('currency',
                    'value',
                    'relation',
                    'date',
                    )
    search_fields = ('currency',)
    ordering = ('date',)


admin.site.register(Code)
admin.site.register(Country, CountryAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Features, FeaturesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Course, CourseAdmin)
