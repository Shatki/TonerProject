# -*- coding: utf-8 -*-
# from io import BytesIO
import os
from TonerProject.settings import BASE_DIR, STATIC_URL, DOCUMENT_DIR
from io import StringIO

# общие
from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect
from datetime import datetime
from document.models import Consignment

# forms
from forms.forms import Form


# Заготовка функции печати первичных форм
def invoice(request, invoice_id):
    # Создаём объект HttpResponse с соответствующим PDF заголовком.
    # response = HttpResponse(content_type='application/pdf',  charset='utf-8')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    pdf_file_name = 'invoice-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.pdf'
    pdf_file = os.path.join(BASE_DIR, 'static', 'documents', pdf_file_name)

    buffer = StringIO()
    # Создаём объект PDF, используя объект HttpResponse как файл.
    doc = canvas.Canvas(pdf_file, pagesize=portrait(A4))

    width, height = A4
    print(width, height)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    pdfmetrics.registerFont(TTFont('Arial', os.path.join(BASE_DIR, 'forms', 'fonts', 'Arial_Cyr.ttf')))

    doc.setFont('Arial', 8)

    doc.drawString(33 * mm, 9 * mm,
                   u'Внимание! Оплата данного счета означает согласие с условиями поставки товара. Уведомление об оплате')
    doc.drawString(33 * mm, 10 * mm,
                   u'обязательно, в противном случае не гарантируется наличие товара на складе. Товар отпускается по факту')
    doc.drawString(33 * mm, 20 * mm,
                   u'прихода денег на р/с Поставщика, самовывозом, при наличии доверенности и паспорта.')

    doc.setLineWidth(1)
    # doc.line(480, 747, 580, 747)



    # Close the PDF object cleanly.
    doc.showPage()
    doc.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    # request.write(pdf)

    # Строим страницу и отправляем
    args = {
        'title': 'Счет на оплату',
        'file_name': DOCUMENT_DIR + pdf_file_name,
    }
    return render_to_response('pdf.html', args)


def torg12(request, consignment_id):
    """ Читаем накладную из БД """
    try:
        consignment = Consignment.objects.get(id=consignment_id)
    except Consignment.DoesNotExist:
        return False
    # Подготавливаем данные
    context = {
        'document_title': 'Накладная',
        'document_number': consignment.number,
        'document_date': consignment.date,
        'product': consignment.items,

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
