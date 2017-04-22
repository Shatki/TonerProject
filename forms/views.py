# -*- coding: utf-8 -*-
# from io import BytesIO
import os
from TonerProject.settings import BASE_DIR, STATIC_URL, DOCUMENT_DIR
from io import StringIO
from document.models import Consignment, ConsignmentTable

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
    for get_one in items:
        obj = dict(
            id=str(get_one.id),
            name=str(get_one.product),
            measure=str(get_one.measure),
            quantity=str(get_one.quantity),
            country=str(get_one.country),
            code=str(get_one.serial_number),
            OKEI=str(get_one.measure.OKEI),
            tax='Без НДС',
            cost_tax='-',

            # cost=str(get_one.cost),
            # total=str(get_one.total),
        )
        rows.append(obj)

    context = {
        'document_title': 'Накладная',
        'document_number': consignment.number,
        'emitter': consignment.emitter,
        'receiver': consignment.receiver,
        'payer': consignment.receiver,
        'contract': consignment.contract,
        'document_date': consignment.date.strftime('%d.%m.%Y'),
        # 'total': data['total'],
        'rows': rows,
    }
    """ создаём наименование PDF файла """
    pdf_file_name = 'consignment' + datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + '.pdf'
    # создаем PDF файл документа для отдачи
    pdf_file = os.path.join(BASE_DIR, 'static', 'documents', pdf_file_name)

    # Отправляем их в шаблом
    print_form = Form(pdf_file, context)
    print_form.load_xlsx(os.path.join(BASE_DIR, 'forms', 'forms', 'torg12.xlsx'), u'torg12')
    print_form.render()

    # return HttpResponse(pdf_file, content_type='application/pdf')
    return redirect(os.path.join(STATIC_URL, DOCUMENT_DIR + pdf_file_name))
