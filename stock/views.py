# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.template.context_processors import csrf
from django.contrib import auth
from system.models import Category, Product
from stock.models import Package, Item


# AJAX запрос для формы.
@csrf_protect
def package_json(request):
    response = []
    try:
        packages = Package.objects.all()
    except Package.DoesNotExist:
        return HttpResponse(u"package_json. BD Error", content_type='text/html')
    for package in packages:
        elem = dict(
            id=str(package.id),
            name=package.name,
        )
        response.append(elem)
    return JsonResponse(response, safe=False)


# AJAX Запрос информации о товаре с id=item_id
@csrf_protect
def item_json(request, item_id):
    # AJAX Запрос на получение реквизитов товара
    # добавить проверку на пользователя
    # Редактирование накладной
    if item_id:
        try:
            item = Item.objects.get(id=item_id)
            response = dict(product='p' + str(item.product_id),
                            country=item.country_id,
                            warranty=item.warranty,
                            package=item.package_id,
                            serial_number=item.serial_number,
                            quantity=item.quantity,
                            measure=item.measure_id,
                            status='Ok',
                            )
            return JsonResponse(response, safe=False)
        except:
            return HttpResponse("item_json: DB Error", content_type='text/html')
    return HttpResponse("item_json: request error", content_type='text/html')


# Добавление нового товара а БД. Вызвывется из app.document
@csrf_protect
def item_add(request, product_id):
    # Добавление нового товара
    try:
        new_item = Item.objects.create(
            product=Product.objects.get(id=product_id),
            country_id=request.POST.get('country'),
            warranty=request.POST.get('warranty'),
            package_id=request.POST.get('package'),
            serial_number=int(request.POST.get('serial_number')),
            quantity=float(request.POST.get('quantity')),
            measure_id=request.POST.get('measure'),
        )
    except Item.DoesNotExist:
        return False
    return new_item


# Редактирование характеристик или данных о товаре
@csrf_protect
def item_edit(request, item_id):
    # Внесение изменений в товар
    try:
        item = Item.objects.get(id=item_id)
        item.product_id = request.POST.get('product')[1:]
        item.country_id = request.POST.get('country')
        item.warranty = request.POST.get('warranty')
        item.package_id = request.POST.get('package')
        item.serial_number = int(request.POST.get('serial_number'))
        item.quantity = float(request.POST.get('quantity'))
        item.measure_id = request.POST.get('measure')
        item.save()
    except Item.DoesNotExist:
        return HttpResponse("item_edit: DB Error", content_type='text/html')
    return HttpResponse("Ok", content_type='text/html')


# Удаление товара из БД. Вызывается из document.consignment.consignment_item_delete. Требует доработки.
def item_delete(item_id):
    # Удаление накладной(только админ)
    try:
        Item.objects.get(id=item_id).delete()
    except Item.DoesNotExist:
        return False
    return True
