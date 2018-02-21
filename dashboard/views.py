# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

from contractor.models import Contractor
from authentication.views import login
from django.views.decorators.csrf import ensure_csrf_cookie
from system.models import Product, Measure
from system.datetime import SystemDateTime

# from TonerProject.settings import STATIC_URL


# Create your views here.

# Представление общего журнала накладных
@csrf_protect
@login_required
def dashboard(request):
    # добавить проверку на пользователя
    try:
        args = {'user_profile': request.user,
                # 'documents': Document.objects.filter(delete=False),
                'contractors': Contractor.objects.all(),
                'measures': Measure.objects.all(),
                'system_date': SystemDateTime.today(),
                }
    except:
        return HttpResponse(u'dashboard: DB Error', content_type='text/html')
    args.update(csrf(request))
    # просмотр полного списка накладных
    return render_to_response('dashboard.html', args)


def testpage(request):
    return render_to_response('test.html', testpage)
