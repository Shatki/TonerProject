# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import JsonResponse

from contractor.models import Contractor
from system.models import Product, Measure, Country
from .models import Consignment, ConsignmentTable
from stock.models import Item
from stock.views import item_add, item_delete


# Представление общего журнала накладных
@csrf_protect
def consignments(request):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                'consignments': Consignment.objects.all(),
                'contractors': Contractor.objects.all(),
                'measures': Measure.objects.all()
                }

    except:
        return HttpResponse(u"consignments: DB Error", content_type='text/html')
    args.update(csrf(request))

    # просмотр полного списка накладных
    return render_to_response('consignments.html', args)


# JSON обработка отображение общего журнала
@csrf_protect
def consignments_json(request):
    try:
        data = Consignment.objects.all()
    except:
        return HttpResponse(u'consignments_json: DB Error', content_type='text/html')
    # Serialize
    rows = []
    for get_one in data:
        obj = dict(
            id=str(get_one.id),
            name=str(get_one),
            seller=str(get_one.emitter),
            buyer=str(get_one.receiver),
            status=str(get_one.status),
        )
        rows.append(obj)
    # final preparing
    response = dict(
        total=str(data.count()),
        rows=rows,
    )

    return JsonResponse(response, safe=False)


# Отображение представление одной накладной
@csrf_protect
def consignment_edit(request, consignment_id):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                'consignment': Consignment.objects.get(id=consignment_id),
                'contractors': Contractor.objects.all(),
                # 'items': Consignment.objects.get(id=consignment_id).items.all(),
                'measures': Measure.objects.all(),
                }

    except:
        return HttpResponse(u"consignment_edit: DB error", content_type='text/html')
    args.update(csrf(request))
    # просмотр полного списка накладных
    return render_to_response('consignment.html', args)


# Тестовая версия создания накладной
@csrf_protect
def consignment_new(request):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                'contractors': Contractor.objects.all(),
                'products': Product.objects.all(),
                'measures': Measure.objects.all(),
                }
    except:
        return HttpResponse(u'consignment_new:  DB error', content_type='text/html')
    # if request.user.contractor_id is not None:
    #    args['contractor'] = Contractor.objects.get(id=request.user.contractor_id)
    args.update(csrf(request))

    # Добавление новой накладной
    return render_to_response("consignment.html", args)


# JSON обработка отображение позиций товара
@csrf_protect
def consignment_items_json(request, consignment_id):
    try:
        items = Consignment.objects.get(id=consignment_id).items.all()
    except:
        return HttpResponse(u'items_json: Error DB', content_type='text/html')
    # Serialize
    rows = []
    for get_one in items:
        obj = dict(
            id=str(get_one.id),
            name=str(get_one),
            measure=str(get_one.measure),
            quantity=str(get_one.quantity),
            country=str(get_one.country),
            # cost=str(get_one.cost),
            # total=str(get_one.total),
        )
        rows.append(obj)
    # final preparing
    response = dict(
        total=str(items.count()),
        rows=rows,
    )

    return JsonResponse(response, safe=False)


# Создание нового товара и добавление его в накладную
@csrf_protect
def consignment_item_add(request, consignment_id):
    if request.POST and consignment_id and request.POST.get('product'):
        # Нужно добавить больше валидаций данных
        if request.POST.get('product')[0] != 'p':
            return HttpResponse("consignment_item_add: AJAX data error", content_type='text/html')
        product_id = request.POST.get('product')[1:]
        # Возможно нужно перенести часть функции в stock.view.item_add
        try:
            new_item = item_add(request, product_id)
            if new_item:
                ConsignmentTable.objects.create(
                    item=new_item,
                    consignment_id=consignment_id,
                )
            else:
                return HttpResponse("item_add: DB error", content_type='text/html')
        except:
            return HttpResponse("consignment_item_add: DB error", content_type='text/html')
        # response.update(csrf(request))
        return HttpResponse("Ok", content_type='text/html')
    else:
        return HttpResponse("consignment_item_add: AJAX data error", content_type='text/html')


# Удаление товара из накладной и из базы
# Пробная версия
@csrf_protect
def consignment_item_delete(request, consignment_id, item_id):
    if consignment_id and item_id:
        try:
            # Удаляем запись о товаре в накладной из базы
            ConsignmentTable.objects.get(item_id=item_id, consignment_id=consignment_id).delete()

            # тут основной функционал, многое надо допилить
            # Удаляем товар!! очень аккуратно
            if not item_delete(item_id):
                return HttpResponse("item_delete: Can't delete Item", content_type='text/html')
        except ConsignmentTable.DoesNotExist:
            return HttpResponse("consignment_item_delete: ConsignmentTable.DoesNotExist", content_type='text/html')
        return HttpResponse("Ok", content_type='text/html')
    return HttpResponse("consignment_item_delete: AJAX data error", content_type='text/html')
