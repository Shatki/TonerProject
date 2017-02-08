# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, JsonResponse
from django.template.context_processors import csrf
from django.contrib import auth
from system.models import Category, Product
from stock.models import Package


# Create your views here.
def package_json(request):
    response = []
    try:
        packages = Package.objects.all()
    except Package.DoesNotExist:
        return HttpResponse(u"Ошибка package_json. Ошибка БД", content_type='text/html')
    for package in packages:
        elem = dict(
            id=str(package.id),
            name=package.name,
        )
        response.append(elem)
    return JsonResponse(response, safe=False)


def add(request):
    # Добавление новой накладной
    return render_to_response('add.html', )


def edit(request):
    # Редактирование накладной
    return render_to_response('add.html', )


def delete(request):
    # Удаление накладной(только админ)
    return render_to_response('add.html', )
