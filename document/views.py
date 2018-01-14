# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

from contractor.models import Contractor
from system.models import Product, Measure
from .models import Consignment, ConsignmentTable
from stock.views import item_add, item_edit, item_delete
from system.datetime import SystemDateTime
from datetime import datetime, timedelta

from RUSystem.RUClient import send_data


# Представление общего журнала накладных
@csrf_protect
@login_required
def consignments(request):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                # 'consignments': Consignment.objects.filter(delete=False),
                'contractors': Contractor.objects.all(),
                'measures': Measure.objects.all(),
                'system_date': SystemDateTime.today(),
                }
    except:
        return HttpResponse(u"journal: DB Error", content_type='text/html')
    args.update(csrf(request))
    # просмотр полного списка накладных
    return render_to_response('journal.html', args)


# JSON запрос элементов для отображения журнала накладных
@csrf_protect
@login_required
def consignments_json(request):
    # Нужно ограничить количество запросов в секунду

    try:
        docs_datetime_to = request.POST.get('dateTo')
        docs_datetime_from = request.POST.get('dateFrom')

        # Если еще не предоставлена дата
        if not docs_datetime_to:
            docs_datetime_to = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            # Дата получена из запроса - преобразуем ее из JS формата в Python
            docs_datetime_to = datetime.strptime(docs_datetime_to, "%d/%m/%Y %H:%M:%S")

        if not docs_datetime_from:
            # Если не указана дата берем диапазон 90 дней
            docs_datetime_from = docs_datetime_to - timedelta(days=90, hours=0, minutes=0, seconds=0, microseconds=0)
        else:
            # Дата получена из запроса - преобразуем ее из JS формата в Python
            docs_datetime_from = datetime.strptime(docs_datetime_from, "%d/%m/%Y %H:%M:%S")

        # Показывает только не удаленные

        data = Consignment.objects.filter(delete=False, date__range=[docs_datetime_from, docs_datetime_to])
    except Consignment.DoesNotExist:
        return HttpResponse(u'consignments_json: DB Error', content_type='text/html')
    # Serialize
    rows = []
    for get_one in data:
        obj = dict(
            id=str(get_one.id),
            name=str(get_one),
            seller=str(get_one.emitter),
            buyer=str(get_one.receiver),
            enable=str(get_one.enable),
            delete=str(get_one.delete),
        )
        rows.append(obj)
    # final preparing
    response = dict(
        total=str(data.count()),
        date_from=docs_datetime_from.strftime("%d/%m/%Y %H:%M:%S"),
        date_to=docs_datetime_to.strftime("%d/%m/%Y %H:%M:%S"),
        date_request=datetime.today().strftime("%d/%m/%Y %H:%M:%S"),
        rows=rows,
    )
    return JsonResponse(response, safe=False)


# Сохранение накладной  через POST
@csrf_protect
@login_required
def consignment_save(request, consignment_id):
    try:
        consignment = Consignment.objects.get(id=consignment_id)
        # Предобработка данных
        if not request.POST.get('date'):
            return HttpResponse("consignment_save: Error received data", content_type='text/html')
        # Обработка даты
        consignment.date = SystemDateTime.decode(request.POST.get('date'))
        consignment.number = request.POST.get('number')
        consignment.emitter_id = Contractor.objects.get(name=request.POST.get('emitter')).id
        consignment.receiver_id = Contractor.objects.get(name=request.POST.get('receiver')).id
        consignment.modified = datetime.today()
        consignment.modificator = request.user
        consignment.delete = False
        consignment.save()
    except:
        return HttpResponse(u"consignment_save: DB error", content_type='text/html')
    # args.update(csrf(request))
    # просмотр полного списка накладных
    return HttpResponse("Ok", content_type='text/html')


# Удаление накладной  через POST
@csrf_protect
@login_required
def consignment_delete(request, consignment_id):
    try:
        # Мягкое удаление
        doc = Consignment.objects.get(id=consignment_id)
        doc.delete = True
        doc.save()
        # Жесткое удаление
        # Consignment.objects.filter(id=consignment_id).delete()
        # Предобработка данных
    except Consignment.DoesNotExist:
        return HttpResponse(u"consignment_delete: DB error", content_type='text/html')
    # args.update(csrf(request))
    # просмотр полного списка накладных
    return HttpResponse("Ok", content_type='text/html')


# Отображение представления одной накладной
@csrf_protect
@login_required
def consignment_edit(request, consignment_id):
    # добавить проверку на пользователя
    if request.user:
        try:
            consignment = Consignment.objects.get(id=consignment_id)
        except Consignment.DoesNotExist:
            consignment = dict(
                id='0'
            )
        args = {'user_profile': request.user,
                'consignment': consignment,
                'contractors': Contractor.objects.all(),
                # 'items': Consignment.objects.get(id=consignment_id).items.all(),
                'measures': Measure.objects.all(),
                }
        args.update(csrf(request))
        # просмотр полного списка накладных
        return render_to_response('document.html', args)
    else:
        return HttpResponse(u'consignment_edit:  please, login first', content_type='text/html')

# Тестовая версия создания накладной
@csrf_protect
@login_required
def consignment_new(request):
    # добавить проверку на пользователя
    try:
        new_consignment = Consignment.objects.create(
            date=SystemDateTime.db_today(),
            creator=request.user,
            modificator=request.user,
        )
        args = {'user_profile': request.user,
                'consignment': new_consignment,
                'creator': request.user,
                'modificator': request.user,
                'contractors': Contractor.objects.all(),
                'products': Product.objects.all(),
                'measures': Measure.objects.all(),
                }
    except:
        return HttpResponse(u'consignment_new:  DB error', content_type='text/html')
    if request.user.contractor_id is not None:
        args["contractor"] = Contractor.objects.get(id=request.user.contractor_id)
    args.update(csrf(request))

    # Добавление нового документа
    return render_to_response("document.html", args)


# JSON обработка отображение позиций товара
@csrf_protect
@login_required
def consignment_items_json(request, consignment_id):
    try:
        items = ConsignmentTable.objects.filter(consignment_id=consignment_id).all()
        # rows = ConsignmentTable.objects.
    except ConsignmentTable.DoesNotExist:
        return HttpResponse(u'items_json: Error DB', content_type='text/html')
    # Serialize
    rows = []
    item_id = 0
    for get_one in items:
        item_id += 1
        obj = dict(
            itemId=str(item_id),
            itemName=str(get_one.item),
            productId=str(get_one.id),
            measure=str(get_one.measure),
            quantity=str(get_one.quantity),
            country=str(get_one.country),
            cost=str(get_one.cost),
            tax=str(get_one.tax.value * get_one.cost),
            total=str(get_one.quantity * get_one.cost),
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
@login_required
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
                Consignment.items.create(  # ????
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


# Дублирование товара из сохраненного в куках и добавление его в накладную
@csrf_protect
@login_required
def consignment_item_paste(request, consignment_id):
    if request.POST and consignment_id and request.POST.get('item'):
        # Возможно нужно перенести часть функции в stock.view.item_add
        try:
            consignment_id = Consignment.objects.get(id=consignment_id).id

            if consignment_id:
                Consignment.items.create(
                    item=get_item,  # Недоделал еще
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


@csrf_protect
@login_required
def consignment_item_edit(request, consignment_id, item_id):
    if request.POST and consignment_id and item_id and request.POST.get('product'):
        # Нужно добавить больше валидаций данных
        if request.POST.get('product')[0] != 'p':
            return HttpResponse("consignment_item_edit: AJAX data error", content_type='text/html')
        # Возможно нужно перенести часть функции в stock.view.item_edit
        return item_edit(request, item_id)


# Удаление товара из накладной и из базы
# Пробная версия
@csrf_protect
@login_required
def consignment_item_delete(request, consignment_id, item_id):
    if consignment_id and item_id:
        try:
            # Удаляем запись о товаре в накладной из базы
            Consignment.items.get(item_id=item_id, consignment_id=consignment_id).delete()

            # тут основной функционал, многое надо допилить
            # Удаляем товар!! очень аккуратно
            if not item_delete(item_id):
                return HttpResponse("item_delete: Can't delete Item", content_type='text/html')
        except Consignment.DoesNotExist:
            return HttpResponse("consignment_item_delete: ConsignmentTable.DoesNotExist", content_type='text/html')
        return HttpResponse("Ok", content_type='text/html')
    return HttpResponse("consignment_item_delete: AJAX data error", content_type='text/html')
