# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth
from django.http import JsonResponse


# Create your views here.
def items_json(request):
    # Добавление новой накладной
    response = [{
        "id": 1,
        "text": "Folder1",
        "iconCls": "icon-save",
        "children": [{
            "text": "File1",
            "checked": True,
        }, {
            "text": "Books",
            "state": "open",
            "attributes": {
                "url": "/",
                "price": 100,
            },
            "children": [{
                "id": 67,
                "text": "PhotoShop",
                "checked": True,
            }, {
                "text": "Sub Books",
                "state": "close"
            }]
        }]
    }, {
        "text": "Languages",
        "state": "closed",
        "children": [{
            "text": "Java"
        }, {
            "text": "C#"
        }]
    }]
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
