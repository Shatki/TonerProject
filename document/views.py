# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect

from contractor.models import Contractor
from stock.views import item_add, item_edit, item_delete
from system.datetime import SystemDateTime
from system.models import Product, Measure
from .models import Document, DocumentTable

# JSON запрос элементов для отображения журнала накладных
@csrf_protect
@login_required
def documents_json(request, doctype):
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

        data = Document.objects.filter(delete=False, date__range=[docs_datetime_from, docs_datetime_to])
    except Document.DoesNotExist:
        return HttpResponse(u'documents_json: DB Error', content_type='text/html')
    # Serialize
    rows = []
    for get_one in data:
        obj = dict(
            id=str(get_one.id),
            number=str(get_one.number),
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
def document_save(request, doctype, document_id):
    try:
        document = Document.objects.get(id=document_id)
        # Предобработка данных
        if not request.POST.get('date'):
            return HttpResponse("Document_save: Error received data", content_type='text/html')
        # Обработка даты
        Document.date = SystemDateTime.decode(request.POST.get('date'))
        Document.number = request.POST.get('number')
        Document.emitter_id = Contractor.objects.get(name=request.POST.get('emitter')).id
        Document.receiver_id = Contractor.objects.get(name=request.POST.get('receiver')).id
        Document.modified = datetime.today()
        Document.modificator = request.user
        Document.delete = False
        Document.save()
    except:
        return HttpResponse(u"Document_save: DB error", content_type='text/html')
    # args.update(csrf(request))
    # просмотр полного списка накладных
    return HttpResponse("Ok", content_type='text/html')


# Удаление накладной  через POST
@csrf_protect
@login_required
def document_delete(request, doctype, document_id):
    try:
        # Мягкое удаление
        doc = Document.objects.get(id=document_id)
        doc.delete = True
        doc.save()
        # Жесткое удаление
        # Document.objects.filter(id=Document_id).delete()
        # Предобработка данных
    except Document.DoesNotExist:
        return HttpResponse(u"Document_delete: DB error", content_type='text/html')
    # args.update(csrf(request))
    # просмотр полного списка накладных
    return HttpResponse("Ok", content_type='text/html')


# Отображение представления одной накладной
@csrf_protect
@login_required
def document_edit(request, doctype, document_id):
    # добавить проверку на пользователя
    if request.user:
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            document = dict(
                id='0'
            )
        args = {'user_profile': request.user,
                'document': document,
                'contractors': Contractor.objects.all(),
                #'items': Document.objects.get(id=document_id).items.all(),
                'measures': Measure.objects.all(),
                }
        args.update(csrf(request))
        # просмотр полного списка накладных
        return render_to_response('document.html', args)
    else:
        return HttpResponse(u'document_edit:  please, login first', content_type='text/html')

# Тестовая версия создания накладной
@csrf_protect
@login_required
def document_new(request, doctype):
    # добавить проверку на пользователя
    # Просто для отладки фронтэнда возвращаем одно значение 31
    response = dict(
        index=str('31'),
        date=SystemDateTime.db_today().strftime("%d/%m/%Y %H:%M:%S"),
    )
    """
            try:
                new_document = Document.objects.create(
                    date=SystemDateTime.db_today(),
                    creator=request.user,
                    modificator=request.user,
                )
                args = {'user_profile': request.user,
                        'Document': new_document,
                        'creator': request.user,
                        'modificator': request.user,
                        'contractors': Contractor.objects.all(),
                        'products': Product.objects.all(),
                        'measures': Measure.objects.all(),
                        }
            except:
                return HttpResponse(u'Document_new:  DB error', content_type='text/html')
            if request.user.contractor_id is not None:
                args["contractor"] = Contractor.objects.get(id=request.user.contractor_id)
            args.update(csrf(request))

            # Добавление нового документа
            return render_to_response("document.html", args)
    """
    return JsonResponse(response, safe=False)



# Создание документа по образу и подобию заданного
@csrf_protect
@login_required
def document_copy_json(request, doctype, document_id):
    # добавить проверку на пользователя
    try:
        items = DocumentTable.objects.filter(document_id=document_id).all()
        new_document = Document.objects.create(
            date=SystemDateTime.db_today(),
            creator=request.user,
            modificator=request.user,
            items=items,
        )
        args = {'user_profile': request.user,
                'Document': new_document,
                'creator': request.user,
                'modificator': request.user,
                'contractors': Contractor.objects.all(),
                'products': Product.objects.all(),
                'measures': Measure.objects.all(),
                }
    except:
        return HttpResponse(u'Document_new:  DB error', content_type='text/html')
    if request.user.contractor_id is not None:
        args["contractor"] = Contractor.objects.get(id=request.user.contractor_id)
    args.update(csrf(request))

    # Добавление нового документа
    return render_to_response("document.html", args)


# JSON обработка отображение позиций товара
@csrf_protect
@login_required
def document_items_json(request, doctype, document_id):
    try:
        items = DocumentTable.objects.filter(document_id=document_id).all()
        # rows = DocumentTable.objects.
    except DocumentTable.DoesNotExist:
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
def document_item_add(request, doctype, document_id):
    if request.POST and document_id and request.POST.get('product'):
        # Нужно добавить больше валидаций данных
        if request.POST.get('product')[0] != 'p':
            return HttpResponse("Document_item_add: AJAX data error", content_type='text/html')
        product_id = request.POST.get('product')[1:]
        # Возможно нужно перенести часть функции в stock.view.item_add
        try:
            new_item = item_add(request, product_id)
            if new_item:
                document.items.create(  # ????
                    item=new_item,
                    document_id=document_id,
                                           )
            else:
                return HttpResponse("item_add: DB error", content_type='text/html')
        except:
            return HttpResponse("Document_item_add: DB error", content_type='text/html')
        # response.update(csrf(request))
        return HttpResponse("Ok", content_type='text/html')
    else:
        return HttpResponse("Document_item_add: AJAX data error", content_type='text/html')


# Дублирование товара из сохраненного в буффере и добавление его в накладную
@csrf_protect
@login_required
def document_item_paste(request, doctype, document_id):
    if request.POST and document_id and request.POST.get('item'):
        # Возможно нужно перенести часть функции в stock.view.item_add
        try:
            document_id = Document.objects.get(id=document_id).id

            if document_id:
                document.items.create(
                    item=get_item,  # Недоделал еще
                    document_id=document_id,
                )
            else:
                return HttpResponse("item_add: DB error", content_type='text/html')
        except:
            return HttpResponse("Document_item_add: DB error", content_type='text/html')
        # response.update(csrf(request))
        return HttpResponse("Ok", content_type='text/html')
    else:
        return HttpResponse("Document_item_add: AJAX data error", content_type='text/html')


@csrf_protect
@login_required
def document_item_edit(request, doctype, document_id, item_id):
    if request.POST and document_id and item_id and request.POST.get('product'):
        # Нужно добавить больше валидаций данных
        if request.POST.get('product')[0] != 'p':
            return HttpResponse("Document_item_edit: AJAX data error", content_type='text/html')
        # Возможно нужно перенести часть функции в stock.view.item_edit
        return item_edit(request, item_id)


# Удаление товара из накладной и из базы
# Пробная версия
@csrf_protect
@login_required
def document_item_delete(request, doctype, document_id, item_id):
    if document_id and item_id:
        try:
            # Удаляем запись о товаре в накладной из базы
            Document.items.get(item_id=item_id, document_id=document_id).delete()

            # тут основной функционал, многое надо допилить
            # Удаляем товар!! очень аккуратно
            if not item_delete(item_id):
                return HttpResponse("item_delete: Can't delete Item", content_type='text/html')
        except Document.DoesNotExist:
            return HttpResponse("document_item_delete: DocumentTable.DoesNotExist", content_type='text/html')
        return HttpResponse("Ok", content_type='text/html')
    return HttpResponse("document_item_delete: AJAX data error", content_type='text/html')
