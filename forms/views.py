# -*- coding: utf-8 -*-
# from io import BytesIO
import os
from TonerProject.settings import BASE_DIR, STATIC_URL, DOCUMENT_DIR
from io import StringIO
from document.models import Consignment
import cProfile

# общие
from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
from document.models import Consignment
from document.views import consignment_items_json

# forms
from forms.forms import Form


# Заготовка функции печати первичных форм
def invoice(request, invoice_id):
    return


def torg12(request, consignment_id):
    """ Читаем накладную из БД """
    try:
        consignment = Consignment.objects.get(id=consignment_id)
        items = Consignment.objects.get(id=consignment_id).items.all()
    except Consignment.DoesNotExist:
        return False
    # Подготавливаем данные в шаблон
    # Serialize
    rows = []
    for item in items:
        obj = dict(
            id=str(item.id),
            name=str(item.product),
            measure=str(item.measure),
            quantity=str(item.quantity),
            country=str(item.country),
            code=str(item.id),  # Тут нужен артикул товара
            OKEI=str(item.measure.OKEI),
            cost='1000.00',
            cost_without_tax='1000.00',
            tax='c НДС',
            cost_tax='24.00',
            cost_with_tax='1024.00',
            # cost=str(item.cost),
            # total=str(item.total),
        )
        rows.append(obj)

    context = {
        'document_title': 'Накладная',
        'document_number': consignment.number,
        'company': consignment.emitter,
        'emitter': consignment.emitter,
        'receiver': consignment.receiver,
        'payer': consignment.receiver,
        'contract': consignment.contract,
        'document_date': consignment.date.strftime('%d.%m.%Y'),
        'emitter_boss_position': 'Руководитель',
        'emitter_position': 'Менеджер',
        'rows': rows,
    }
    """ создаём наименование PDF файла """
    pdf_file_name = 'consignment' + datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + '.pdf'
    # создаем PDF файл документа для отдачи
    pdf_file = os.path.join(BASE_DIR, 'static', 'documents', pdf_file_name)

    # Отправляем их в шаблом
    print_form = Form(pdf_file, context)
    print_form.load_template(os.path.join(BASE_DIR, 'forms', 'forms', 'torg12.xlsx'), )
    print_form.render()

    # return HttpResponse(pdf_file, content_type='application/pdf')
    return redirect(os.path.join(STATIC_URL, DOCUMENT_DIR + pdf_file_name))
