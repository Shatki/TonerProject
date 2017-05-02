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
            code=str(get_one.id),  # Тут нужен артикул товара
            OKEI=str(get_one.measure.OKEI),
            cost='1000.00',
            cost_without_tax='1000.00',
            tax='c НДС',
            cost_tax='24.00',
            cost_with_tax='1024.00',

            # cost=str(get_one.cost),
            # total=str(get_one.total),
        )
        rows.append(obj)

    context = {
        'document_title': 'Накладная',
        'document_number': consignment.number,
        'company': 'I understand (I think). Please explain how the wanted value is specified. Is it a (the only) leaf in the tree which fits a certain condition? What is this condition? To perform a search in a tree you can use breadth-search or depth-search or a more custom-tailored variant. But I need to know more about the situation you are in to give qualified advice. ',
        'emitter': 'I understand (I think). Please explain how the wanted value is specified. Is it a (the only) leaf in the tree which fits a certain condition? What is this condition? To perform a search in a tree you can use breadth-search or depth-search or a more custom-tailored variant. But I need to know more about the situation you are in to give qualified advice. ',
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
    print_form.load_xlsx(os.path.join(BASE_DIR, 'forms', 'forms', 'torg12.xlsx'), u'torg12')
    print_form.render()

    # return HttpResponse(pdf_file, content_type='application/pdf')
    return redirect(os.path.join(STATIC_URL, DOCUMENT_DIR + pdf_file_name))
