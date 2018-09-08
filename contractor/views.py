# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import JsonResponse
# import time

from .models import Contractor


def contractors_json(request):
    response = []
    try:
        contractors = Contractor.objects.all()
    except Contractor.DoesNotExist:
        return HttpResponse(u"Conteractor.contractor_json. BD error", content_type='text/html')
    for contractor in contractors:
        elem = dict(
            id=str(contractor.id),
            name=contractor.name,
        )
        response.append(elem)
    return JsonResponse(response, safe=False)
