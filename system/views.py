# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth
from django.http import JsonResponse
from system.models import Product, Features, Developer, Type, Country, Category, Measure


# Create your views here.
def product_view(request, product_id):
    args = {}
    args.update(csrf(request))
    prod = Product.objects.get(id=product_id)
    args['product'] = prod
    # args['product_str'] = prod
    args['features'] = prod.features.all()
    args['features_group'] = Type.objects.filter(belongs=prod.category)
    args['username'] = auth.get_user(request).username
    return render_to_response('product.html', args)


def category_view(request, category):
    args = {}
    args.update(csrf(request))
    args['category'] = category
    return render_to_response('category.html', args)


def country_json(request):
    response = []
    try:
        countries = Country.objects.all()
    except Country.DoesNotExist:
        return HttpResponse(u"Ошибка country_json. Ошибка БД", content_type='text/html')
    for country in countries:
        elem = dict(
            id=str(country.id),
            name=country.name,
        )
        response.append(elem)
    return JsonResponse(response, safe=False)


def measure_json(request):
    response = []
    try:
        measures = Measure.objects.all()
    except Measure.DoesNotExist:
        return HttpResponse(u"Ошибка measure_json. Ошибка БД", content_type='text/html')
    for measure in measures:
        elem = dict(
            id=str(measure.id),
            name=measure.name,
        )
        response.append(elem)
    return JsonResponse(response, safe=False)


def products_json(request):
    """
        Обработка POST запроса на предоставление JSON каталога продукции из базы
        Иерархия создается на Фронтэнде
        - При первом запросе, т.е  id = 0 или None выдаем дерево каталога
        - При id > 0 or id != None выдаем содержание родительского узла из базы
    """
    # Запрос содержания узла категории
    node_id = request.POST.get('id')
    response = []
    if not node_id or node_id == 'DIR-0':
        try:
            categories = Category.objects.all().order_by('name')
        except Product.DoesNotExist:
            return HttpResponse(u"Ошибка product_json. Запрос узла %s Ошибка БД" % node_id, content_type='text/html')
        # Сначала идут категории
        for category in categories:
            # Создание обычного элемента категории
            parent_id = 'DIR-' + str(category.parent_id or 0)
            item = dict(
                itemId='DIR-' + str(category.id),
                parentId=parent_id,
                name=str(category),  # Наименование категории
                # iconCls="icon-print",      # Иконка категории, нужна?
                state='closed',
            )
            response.append(item)
    else:
        try:
            products = Product.objects.filter(category_id=node_id[4:]).order_by('name')
        except Product.DoesNotExist:
            return HttpResponse(u"Ошибка product_json. Запрос узла %s Ошибка БД" % node_id, content_type='text/html')
        for product in products:
            # Создание обычного элемента с заполнением его значений
            item = dict(
                itemId='ITM-' + str(product.id),
                parentId=str(node_id or 0),
                name=str(product),  # Наименование продукта
                iconCls="icon-print",  # Иконка продукта, нужна?
                state='open',
            )
            response.append(item)
    return JsonResponse(response, safe=False)


def products_all_json(request):
    # Запрос общего списка продукции в базе
    # с создание JSON иерархии в бэкэнде
    try:
        categories = Category.objects.all()
        products = Product.objects.all().order_by('name')
    except Product.DoesNotExist:
        return HttpResponse(u"Ошибка item_json. Ошибка БД", content_type='text/html')
    response = []
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
                name = str(product)
                # Создание обычного элемента с заполнением его значений
                elem = dict(
                    id='ITEM-' + str(product.id),
                    name=name,  # Наименование продукта
                    iconCls="icon-print",  # Иконка продукта, нужна?
                )
                collect.append(elem)
        if collect:
            # Если у категории есть элементы то добавляем ее в response
            dirs = dict(
                id='c' + str(category.id),
                name=category.name,
                iconCls="icon-save",  # Иконка категории
                children=collect,
            )
            if category.parent:
                lists.append({category.parent.id: dirs})
            else:
                # Корневая директория??? Сюда не должно попадать
                lists.append({
                    'id': 'DIR-' + str(category.id),
                    'name': category.name,
                    'iconCls': "icon-save",  # Иконка категории
                    'children': dirs,
                    # 'checked': True,
                })
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
                        id='DIR-' + str(category.id),
                        name=category.name,
                        iconCls="icon-save",  # Иконка категории
                        children=dirs,
                    )
                    response.append({category.parent.id: dirs})
                    still = True
                else:
                    response.append({
                        'id': 'DIR-' + str(category.id),
                        'name': category.name,
                        'iconCls': "icon-save",  # Иконка категории
                        'children': dirs,
                        # 'checked': True,
                    })
        lists = response
    # print(response)
    return JsonResponse(response, safe=False)


"""
response_ = [{
    'children': [{
        'children': [{
            'iconCls': 'icon-print',
            'id': 5,
            'name': 'Материнская плата Asus M5A78L-M LX3, SocketAM3+, mATX'
        }, {
            'iconCls': 'icon-print',
            'id': 4,
            'name': 'Материнская плата Asus M5A97 LE R2.0, SocketAM3+, mATX'
        }, {
            'iconCls': 'icon-print',
            'id': 3,
            'name': 'Материнская плата ASRock N68-GS4 FX, SocketAM3+, mATX'
        }],
        'iconCls': 'icon-save', 'id': 1, 'name': 'Материнская плата'
    }, {
        'children': [{
            'iconCls':
                'icon-print',
            'id': 2,
            'name': 'Оперативная память Hynix HMT451U6AFR8C, DDR3, 4 Гб, 1600 МГц, DIMM'
        }],
        'iconCls': 'icon-save',
        'id': 3,
        'name': 'Оперативная память'
    }, {
        'children': [{
            'iconCls': 'icon-print',
            'id': 6,
            'name': 'Процессор AMD A8 6600K, SocketFM2'}],
        'iconCls': 'icon-save',
        'id': 2,
        'name': 'Процессор'}],
    'id': '1',
    'name': "C",
    'iconCls': "icon-save"}]  # Иконка категории

response_ = [{
    'id': '1',
    'name': "C",
    'iconCls': "icon-save",  # Иконка категории
    'children': [{
        "id": '2',
        "name": "Program Files",
        "size": "120 MB",
        "date": "03/20/2010",
        "children": [{
            "id": '21',
            "name": "Java",
            "size": "",
            "date": "01/13/2010",
            "state": "closed",
            "children": [{
                "id": '2',
                "name": "java.exe",
                "size": "142 KB",
                "date": "01/13/2010"
            }, {
                "id": '1',
                "name": "jawt.dll",
                "size": "5 KB",
                "date": "01/13/2010"
            }]
        }, {
            "id": 22,
            "name": "MySQL",
            "size": "",
            "date": "01/13/2010",
            "state": "closed",
            "children": [{
                'iconCls': 'icon-print',
                'id': 'p5',
                'name': 'Материнская плата Asus M5A78L-M LX3, SocketAM3+, mATX'
            }, {
                'iconCls': 'icon-print',
                'id': 'p4',
                'name': 'Материнская плата Asus M5A97 LE R2.0, SocketAM3+, mATX'
            }, {
                'iconCls': 'icon-print',
                'id': 'p3',
                'name': 'Материнская плата ASRock N68-GS4 FX, SocketAM3+, mATX'
            }]
        }]
    }, {
        "id": 3,
        "name": "eclipse",
        "size": "",
        "date": "01/20/2010",
        "children": [{
            "id": 31,
            "name": "eclipse.exe",
            "size": "56 KB",
            "date": "05/19/2009"
        }, {
            "id": 32,
            "name": "eclipse.ini",
            "size": "1 KB",
            "date": "04/20/2010"
        }, {
            "id": 33,
            "name": "notice.html",
            "size": "7 KB",
            "date": "03/17/2005"
        }]
    }]
}]

"""
