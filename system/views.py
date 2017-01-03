# -*- coding: utf-8 -*-
from system.models import Product, Features, Developer, Type, Country, Category, Code
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.contrib import auth


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
