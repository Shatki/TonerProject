# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth
from django.http import JsonResponse
from system.models import Category, Product


# Create your views here.
def items_json(request):
    try:
        categories = Category.objects.all()
        products = Product.objects.all().order_by('name')
    except Product.DoesNotExist:
        return HttpResponse(u"Ошибка item_json. Ошибка БД", content_type='text/html')

    lists = []
    for category in categories:
        # создаем подготовительный список
        collect = []
        # Ищем все продукты из этой категории
        # Можно сделать запрос из базы, но как быстрее?
        # Это проверим в будущем
        for product in products:
            cat = product.category
            if cat.id == category.id:
                product_id = str(product.id)
                text = str(product)
                # Создание обычного элемента с заполнением его значений
                elem = dict(
                    id=product_id,
                    text=text,  # Наименование продукта
                    iconCls="icon-print",  # Иконка продукта продукта, нужна?
                )
                collect.append(elem)
        if collect:
            # Если у категории есть элементы то добавляем ее в response
            dirs = dict(
                text=category.name,
                iconCls="icon-save",  # Иконка категории
                children=collect,
            )
            if category.parent:
                lists.append({category.parent.id: dirs})
            else:
                # Корневая директория??? Сюда не должно попадать
                lists.append({
                    'text': category.name,
                    'iconCls': "icon-save",  # Иконка категории
                    'children': dirs,
                    'checked': True,
                })

    test1 = [{4:
                  {'checked': True,
                   'text': 'Материнская плата',
                   'children':
                       [{'text': 'Материнская плата Asus M5A78L-M LX3, SocketAM3+, mATX',
                         'id': '5',
                         'iconCls': 'icon-print'},
                        {'text': 'Материнская плата Asus M5A97 LE R2.0, SocketAM3+, mATX',
                         'id': '4', 'iconCls': 'icon-print'},
                        {'text': 'Материнская плата ASRock N68-GS4 FX, SocketAM3+, mATX',
                         'id': '3', 'iconCls': 'icon-print'}],
                   'iconCls': 'icon-save'}},
             {4:
                  {'checked': True,
                   'text': 'Оперативная память',
                   'children':
                       [{'text': 'Оперативная память Hynix HMT451U6AFR8C, DDR3, 4 Гб, 1600 МГц, DIMM',
                         'id': '2', 'iconCls': 'icon-print'}], 'iconCls': 'icon-save'}},
             {4:
                  {'checked': True,
                   'text': 'Процессор',
                   'children':
                       [{'text': 'Процессор AMD A8 6600K, SocketFM2',
                         'id': '6',
                         'iconCls': 'icon-print'}],
                   'iconCls': 'icon-save'}}]

    # Упаковка и создание иерархии
    still = True
    while still:
        response = []
        still = False
        for category in categories:
            dirs = []
            # print(response)
            # Проходим по всем элементам списка и упаковываем в одну категорию
            for one in lists:
                for key in one.keys():
                    # print(categories.get(id=key))
                    if key == category.id:
                        # print(one[key])
                        dirs.append(one[key])
            # Собрали все элементы
            # Если список не пуст:
            if len(dirs):
                if category.parent:
                    dirs = dict(
                        text=category.name,
                        iconCls="icon-save",  # Иконка категории
                        children=dirs,
                    )
                    response.append({category.parent.id: dirs})
                    still = True
                else:
                    response.append({
                        'text': category.name,
                        'iconCls': "icon-save",  # Иконка категории
                        'children': dirs,
                        'checked': True,
                    })
        lists = response

    test2 = [{5:
                  {'iconCls': 'icon-save',
                   'text': 5,
                   'children':
                       [{'iconCls': 'icon-save',
                         'text': 'Материнская плата',
                         'children':
                             [{'iconCls': 'icon-print',
                               'text': 'Материнская плата Asus M5A78L-M LX3, SocketAM3+, mATX',
                               'id': '5'},
                              {'iconCls': 'icon-print',
                               'text': 'Материнская плата Asus M5A97 LE R2.0, SocketAM3+, mATX',
                               'id': '4'},
                              {'iconCls': 'icon-print',
                               'text': 'Материнская плата ASRock N68-GS4 FX, SocketAM3+, mATX',
                               'id': '3'}]},
                        {'iconCls': 'icon-save',
                         'text': 'Оперативная память',
                         'children':
                             [{'iconCls': 'icon-print',
                               'text': 'Оперативная память Hynix HMT451U6AFR8C, DDR3, 4 Гб, 1600 МГц, DIMM',
                               'id': '2'}]},
                        {'iconCls': 'icon-save',
                         'text': 'Процессор',
                         'children':
                             [{'iconCls': 'icon-print',
                               'text': 'Процессор AMD A8 6600K, SocketFM2',
                               'id': '6'}]}]}},
             {'iconCls': 'icon-save',
              'text': 'Корневая папка',
              'checked': True,
              'children':
                  [{'iconCls': 'icon-save',
                    'text': 5,
                    'children':
                        [{'iconCls': 'icon-save',
                          'text': 'Материнская плата',
                          'children':
                              [{'iconCls': 'icon-print',
                                'text': 'Материнская плата Asus M5A78L-M LX3, SocketAM3+, mATX',
                                'id': '5'},
                               {'iconCls': 'icon-print',
                                'text': 'Материнская плата Asus M5A97 LE R2.0, SocketAM3+, mATX',
                                'id': '4'},
                               {'iconCls': 'icon-print',
                                'text': 'Материнская плата ASRock N68-GS4 FX, SocketAM3+, mATX',
                                'id': '3'}]},
                         {'iconCls': 'icon-save',
                          'text': 'Оперативная память', 'children': [{'iconCls': 'icon-print',
                                                                      'text': 'Оперативная память Hynix HMT451U6AFR8C, DDR3, 4 Гб, 1600 МГц, DIMM',
                                                                      'id': '2'}]},
                         {'iconCls': 'icon-save', 'text': 'Процессор', 'children': [
                             {'iconCls': 'icon-print', 'text': 'Процессор AMD A8 6600K, SocketFM2', 'id': '6'}]}]}]}]

    print(response)
    return JsonResponse(response, safe=False)


# Create your views here.
def add(request):
    # Добавление новой накладной
    return render_to_response('add.html', )


def edit(request):
    # Редактирование накладной
    return render_to_response('add.html', )


def delete(request):
    # Удаление накладной(только админ)
    return render_to_response('add.html', )
