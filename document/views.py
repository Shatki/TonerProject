# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib import auth
from django.http import JsonResponse

from contractor.models import Contractor
from system.models import Product, Measure
from .models import Consignment


# Представление общего журнала накладных
def consignments(request):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                'consignments': Consignment.objects.all(),
                'contractors': Contractor.objects.all(),
                'measures': Measure.objects.all()
                }

    except:
        return HttpResponse(u"Ошибка consignments. Ошибка БД", content_type='text/html')
    args.update(csrf(request))

    # просмотр полного списка накладных
    return render_to_response('consignments.html', args)


# JSON обработка отображение общего журнала
def consignments_json(request):
    try:
        data = Consignment.objects.all()
    except:
        return HttpResponse(u'Ошибка consignments_json. Ошибка БД', content_type='text/html')
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
        return HttpResponse(u"Ошибка consignment. Ошибка БД", content_type='text/html')
    args.update(csrf(request))

    # просмотр полного списка накладных
    return render_to_response('consignment.html', args)


# Тестовая версия создания накладной
def consignment_new(request):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                'contractors': Contractor.objects.all(),
                'products': Product.objects.all(),
                'measures': Measure.objects.all(),
                }
    except:
        return HttpResponse(u'Ошибка consignment_new. Ошибка БД', content_type='text/html')
    # if request.user.contractor_id is not None:
    #    args['contractor'] = Contractor.objects.get(id=request.user.contractor_id)
    args.update(csrf(request))

    # Добавление новой накладной
    return render_to_response("consignment.html", args)


# JSON обработка отображение позиций товара
def items_json(request, consignment_id):
    try:
        items = Consignment.objects.get(id=consignment_id).items.all()
    except:
        return HttpResponse(u'Ошибка consignment_get_all. Ошибка БД', content_type='text/html')
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


@csrf_protect
def item_add(request, consignment_id):
    if request.POST:
        response = request.POST.get('serial_number') + ' ' + request.POST.get('country') + ' ' + str(consignment_id)
        print(response)
        # response.update(csrf(request))
    return HttpResponse("Ok", content_type='text/html')



def edit(request):
    # добавить проверку на пользователя
    # Редактирование накладной
    return render_to_response('', )


def delete(request):
    # добавить проверку на пользователя
    # Удаление накладной(только админ)
    return render_to_response('', )
