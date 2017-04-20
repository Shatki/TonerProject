#!/usr/bin/python
# -*- coding: utf8 -*-
import reportlab
from reportlab import rl_config
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table, TableStyle
from PIL import Image, ImageDraw


def createSampleImage():
    img = Image.new('RGB', (10, 10), '#fff')
    w, h = img.size
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, w - 1, h - 1), outline='#000')
    draw.line((0, 0, w - 1, h - 1), fill='#000')
    draw.line((0, w - 1, h - 1, 0), fill='#000')
    img.save('x.png')


def drawOutline(canvas, x, y, width, height):
    canvas.saveState()
    canvas.setStrokeColorCMYK(0, 0, 0, .2)
    canvas.line(x, y + height, x + width, y + height)
    canvas.line(x, y, x + width, y)
    canvas.setFillColorCMYK(0, 0, 0, .6)
    canvas.circle(x, y, 1, fill=True, stroke=False)
    canvas.restoreState()


def drawTestParagraph(canvas, x, y, width=None, style=None, text='Why?'):
    if width is None:
        width = A4[0] - 2 * x

    if style is None:
        style = ParagraphStyle('normal')

    p = Paragraph(text, style)
    p.wrap(width, y)

    drawOutline(canvas, x, y, p.width, p.height)
    p.drawOn(canvas, x, y)


def drawTestString(canvas, x, y, width=None, style=None, text='Why?'):
    if width is None:
        width = A4[0] - 2 * x

    if style is None:
        style = ParagraphStyle('normal')

    drawOutline(canvas, x, y, width, style.leading)

    canvas.saveState()
    canvas.setFont(style.fontName, style.fontSize)
    canvas.drawString(x, y, text)
    canvas.restoreState()


def drawTestTable(canvas, x, y, width=None, style=None, text='Why?'):
    if width is None:
        width = A4[0] - 2 * x

    if style is None:
        style = ParagraphStyle('normal')

    table_style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), style.fontName),
        ('SIZE', (0, 0), (-1, -1), style.fontSize),
    ])

    table = Table([[text]], style=table_style)
    table.wrap(width, y)
    table.drawOn(canvas, x, y)


def registerTTFont(fontname, filename):
    """Register a TrueType font with ReportLab.

    Clears up the incorrect straight-through mappings that ReportLab 1.19
    unhelpfully gives us.
    """
    registerFont(TTFont(fontname, filename))
    # For some reason pdfmetrics.registerFont for TrueType fonts explicitly
    # calls addMapping with incorrect straight-through mappings.  We thus need
    # to stick our dirty fingers in reportlab's internal data structures and
    # undo those changes so that we can call addMapping with correct values.
    key = fontname.lower()
    del reportlab.lib.fonts._tt2ps_map[key, 0, 0]
    del reportlab.lib.fonts._tt2ps_map[key, 0, 1]
    del reportlab.lib.fonts._tt2ps_map[key, 1, 0]
    del reportlab.lib.fonts._tt2ps_map[key, 1, 1]
    del reportlab.lib.fonts._ps2tt_map[key]


def registerFonts():
    rl_config.TTFSearchPath.append('/usr/share/fonts/truetype/msttcorefonts')

    registerTTFont('Times_New_Roman', 'Times_New_Roman.ttf')
    registerTTFont('Times_New_Roman_Bold', 'Times_New_Roman_Bold.ttf')
    registerTTFont('Times_New_Roman_Italic', 'Times_New_Roman_Italic.ttf')
    registerTTFont('Times_New_Roman_Bold_Italic',
                   'Times_New_Roman_Bold_Italic.ttf')

    addMapping('Times_New_Roman', 0, 0, 'Times_New_Roman')
    addMapping('Times_New_Roman', 0, 1, 'Times_New_Roman_Italic')
    addMapping('Times_New_Roman', 1, 0, 'Times_New_Roman_Bold')
    addMapping('Times_New_Roman', 1, 1, 'Times_New_Roman_Bold_Italic')


def draw(filename):
    canvas = Canvas(filename, A4)

    style = ParagraphStyle('normal')

    canvas.drawString(25, 800, 'ReportLab %s, default font (%s, %spt)'
                      % (reportlab.Version, style.fontName, style.fontSize))

    x = 100
    y = 750

    img = '<img src="x.png" />'
    u = u'\n{LATIN CAPITAL LETTER E WITH DOT ABOVE}'  # something definitely not in Type 1

    def testCases(y):
        canvas.drawString(x - 50, y + 25, 'canvas.drawString:')
        drawTestString(canvas, x, y, style=style, text=u'Why? ' + u)
        y -= 50

        canvas.drawString(x - 50, y + 25, 'Paragraph.drawOn:')
        drawTestParagraph(canvas, x, y, style=style, text=u'Why? ' + u)
        y -= 50

        canvas.drawString(x - 50, y + 25, 'Paragraph.drawOn, with an image:')
        drawTestParagraph(canvas, x, y, style=style, text=img + 'Why? ' + u)
        y -= 50

        canvas.drawString(x - 50, y + 25, 'Table.drawOn')
        drawTestTable(canvas, x, y, style=style, text='Why? ' + u)
        y -= 50

        canvas.drawString(x - 50, y + 25, 'Table.drawOn, with an image')
        drawTestTable(canvas, x, y, style=style, text=img + 'Why? ' + u)
        y -= 50

        canvas.drawString(x - 50, y + 25, 'Table.drawOn, with a paragraph')
        drawTestTable(canvas, x, y, style=style, text=Paragraph('Why? ' + u,
                                                                style))
        y -= 50

        canvas.drawString(x - 50, y + 25, 'Table.drawOn, with a paragraph and an image')
        drawTestTable(canvas, x, y, style=style, text=Paragraph(img + 'Why? ' + u,
                                                                style))
        y -= 50

        return y

    y = testCases(y)

    style.fontName = 'Times_New_Roman'
    canvas.drawString(x - 75, y + 25, '%s, %spt'
                      % (style.fontName, style.fontSize))
    y -= 25

    y = testCases(y)

    canvas.showPage()
    canvas.save()


def main():
    createSampleImage()
    registerFonts()
    draw('test.pdf')


if __name__ == '__main__':
    main()

"""
def torg12_reportlab(request, consignment_id):
    try:
        consignment = Consignment.objects.get(id=consignment_id)
    except Consignment.DoesNotExist:
        return False

    # Создаем файл
    pdf_file_name = 'consignment-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.pdf'
    pdf_file = os.path.join(BASE_DIR, 'static', 'documents', pdf_file_name)
    buffer = StringIO()
    document = canvas.Canvas(pdf_file, pagesize=landscape(A4))
    # document = SimpleDocTemplate(pdf_file, pagesize=landscape(A4),
    #                             rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    print(width / mm, height / mm)

    # Настраиваем шрифт
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    pdfmetrics.registerFont(TTFont('Arial', os.path.join(BASE_DIR, 'forms', 'fonts', 'Arial_Cyr.ttf')))

    document.setFont('Arial', 7)
    # canvas.rect(x, y, width, height, stroke=1, fill=0)
    document.setLineWidth(1)
    # document.rect(1*mm, 1*mm, 50*mm, 50*mm)

    # elements = []

    data = [
        [u'Номер\nпо\nпорядку', u'Товар', '', u'Единица измерения', '', 'Вид\nупаковки', 'Количество', '',
         'Масса\nбрутто', 'Коли-\nчество\n(масса\nнетто)', 'Цена, руб.\nкоп.', 'Сумма без\nучета НДС,\nруб. коп.',
         'НДС', '', 'Сумма с\nучётом НДС,\nруб.коп.'],
        ['', 'наименование, характеристика, сорт,\nартикул товара', 'код', 'наиме-\nнование', 'код по\nОКЕИ', '',
         'в одном\nместе', 'мест,\nштук', '', '', '', '', 'ставка, %', 'сумма,\nруб. коп.', ''],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    ]

    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        # ('BOX', (0, 0), (-1, 3), 0.5, colors.black),
        ('GRID', (0, 0), (-1, 3), 0.5, colors.black),
        ('SPAN', (0, 0), (0, 1),),  # Номер по порядку
        ('SPAN', (5, 0), (5, 1),),  # Вид упаковки
        ('SPAN', (8, 0), (8, 1),),  # Масса брутто
        ('SPAN', (9, 0), (9, 1),),  # Масса  нетто
        ('SPAN', (10, 0), (10, 1),),  # Цена руб
        ('SPAN', (11, 0), (11, 1),),  # Сумма без НДС
        ('SPAN', (14, 0), (14, 1),),  # Сумма c НДС
        ('SPAN', (1, 0), (2, 0),),  # Товар
        ('SPAN', (3, 0), (4, 0),),  # Ед. изм
        ('SPAN', (6, 0), (7, 0),),  # Количество
        ('SPAN', (12, 0), (13, 0),),  # НДС
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),

        ('BOTTOMPADDING', (6, 0), (7, 0), -2),  # Количество
    ])

    widths = [12.5 * mm, 55 * mm, 14 * mm, 14 * mm, 14 * mm, 14 * mm, 14 * mm, 14 * mm, 14 * mm, 14 * mm,
              20 * mm, 20 * mm, 15 * mm, 19 * mm, 20 * mm]
    heights = [4.1 * mm, 8.2 * mm, 4.1 * mm]

    table = Table(data, colWidths=widths, rowHeights=heights, repeatRows=1)
    table.setStyle(style)

    table_width, table_height = table.wrapOn(document, width, height)

    # print(table_height)
    table.drawOn(document, *coord(10.1, 96.1 + (table_height / mm), mm))

    # Верхнее поле
    document.setFont('Arial', 6)
    document.drawString(x(179.2), y(11.6),
                        u'Унифицированная форма № ТОРГ-12. Утверждена постановлением Госкомстата России от 25.12.98 № 132')





    # Пост обработка и отдача
    document.showPage()
    document.save()
    # html = template.render(context.drawText=context)
    # return redirect(os.path.join(STATIC_URL, DOCUMENT_DIR + pdf_file_name))
    # Строим страницу и отправляем
    args = {
        'title': 'Накладная',
        'file_name': DOCUMENT_DIR + pdf_file_name,
    }
    # return render_to_response('pdf.html', args)
    # return HttpResponse(pdf_file, content_type='application/pdf')
    return redirect(os.path.join(STATIC_URL, DOCUMENT_DIR + pdf_file_name))


def torg12_old(request, consignment_id):
    try:
        consignment = Consignment.objects.get(id=consignment_id)
    except Consignment.DoesNotExist:
        return False

    # Создаем файл

    context = {
        'consignment_id': '1',
        'consignment_date': '31.10.1985',
    }
    template = get_template('torg12.html')
    html = template.render(context=context)

    return HttpResponse(html)

    @classmethod
    def hexpr(cls, text):
        ret = ''
        for t in text:
            ret += hex(ord(t)) + '/'
        return ret    @classmethod
    def hexpr(cls, text):
        ret = ''
        for t in text:
            ret += hex(ord(t)) + '/'
        return ret    @classmethod
    def hexpr(cls, text):
        ret = ''
        for t in text:
            ret += hex(ord(t)) + '/'
        return ret

     @classmethod
    def hexpr(cls, text):
        ret = ''
        for t in text:
            ret += hex(ord(t)) + '/'
        return ret





 @classmethod
    def hexpr(cls, text):
        ret = ''
        for t in text:
            ret += hex(ord(t)) + '/'
        return ret

class PDF(object):
    def __init__(self, page_size=A4, font_face='Helvetica'):
        self.page_size = page_size
        self.font_face = font_face
        self.logo = None

    def format_currency(self,value):
        a = list(str(int(value)))
        for k in range(len(a)-3,0,-3):
            a.insert(k,',')
        a = ''.join(a)
        b = ("%.2f" % (value-int(value)))[2:]
        return "%s.%s" % (a,b)

    def draw(self, invoice, items_page=10):
        # Draws the invoice
        buffer = StringIO()
        invoice_items = invoice['items']
        pages = max((len(invoice_items)-2)/items_page+1,1)
        canvas = canvas.Canvas(buffer, pagesize=self.page_size)
        for page in range(pages):
            canvas.translate(0, 29.7 * cm)
            canvas.setFont(self.font_face, 10)

            canvas.saveState()
            canvas.setStrokeColorRGB(0.9, 0.5, 0.2)
            canvas.setFillColorRGB(0.2, 0.2, 0.2)
            canvas.setFont(self.font_face, 16)
            canvas.drawString(1 * cm, -1 * cm, invoice.get('title',''))
            if self.logo:
                canvas.drawInlineImage(self.logo, 1 * cm, -1 * cm, 250, 16)
            canvas.setLineWidth(4)
            canvas.line(0, -1.25 * cm, 21.7 * cm, -1.25 * cm)
            canvas.restoreState()

            canvas.saveState()
            notes = listify(invoice.get('notes',''))
            textobject = canvas.beginText(1 * cm, -25 * cm)
            for line in notes:
                textobject.textLine(line)
            canvas.drawText(textobject)
            textobject = canvas.beginText(18 * cm, -28 * cm)
            textobject.textLine('Pag.%s/%s' % (page+1,pages))
            canvas.drawText(textobject)
            canvas.restoreState()

            canvas.saveState()
            business_details = listify(invoice.get('from','FROM:'))
            canvas.setFont(self.font_face, 9)
            textobject = canvas.beginText(13 * cm, -2.5 * cm)
            for line in business_details:
                textobject.textLine(line)
            canvas.drawText(textobject)
            canvas.restoreState()

            canvas.saveState()
            client_info = listify(invoice.get('to','TO:'))
            textobject = canvas.beginText(1.5 * cm, -2.5 * cm)
            for line in client_info:
                textobject.textLine(line)
            canvas.drawText(textobject)
            canvas.restoreState()

            textobject = canvas.beginText(1.5 * cm, -6.75 * cm)
            textobject.textLine(u'Invoice ID: %s' % invoice.get('id','<invoice id>'))
            textobject.textLine(u'Invoice Date: %s' % invoice.get('date',datetime.date.today()))
            textobject.textLine(u'Client: %s' % invoice.get('client_name','<invoice client>'))
            canvas.drawText(textobject)

            items = invoice_items[1:][page*items_page:(page+1)*items_page]
            if items:
                data = [invoice_items[0]]
                for item in items:
                    data.append([
                            self.format_currency(x)
                            if isinstance(x,float) else x
                            for x in item])
                righta = [k for k,v in enumerate(items[0])
                          if isinstance(v,(int,float,Decimal))]
                if page == pages-1:
                    total = self.format_currency(invoice['total'])
                else:
                    total = ''
                data.append(['']*(len(items[0])-1)+[total])
                colWidths = [2.5*cm]*len(items[0])
                colWidths[1] = (21.5-2.5*len(items[0]))*cm
                table = Table(data, colWidths=colWidths)
                table.setStyle([
                        ('FONT', (0, 0), (-1, -1), self.font_face),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                        ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
                        ('GRID', (-1, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
                        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                        ]+[('ALIGN',(k,0),(k,-1),'RIGHT') for k in righta])
                tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
                table.drawOn(canvas, 1 * cm, -8 * cm - th)

            if page == pages-1:
                items = invoice['totals'][1:]
                if items:
                    data = [invoice['totals'][0]]
                    for item in items:
                        data.append([
                                self.format_currency(x)
                                if isinstance(x,float) else x
                                for x in item])
                    righta = [k for k,v in enumerate(items[0])
                              if isinstance(v,(int,float,Decimal))]
                    total = self.format_currency(invoice['total'])
                    data.append(['']*(len(items[0])-1)+[total])
                    colWidths = [2.5*cm]*len(items[0])
                    colWidths[1] = (21.5-2.5*len(items[0]))*cm
                    table = Table(data, colWidths=colWidths)
                    table.setStyle([
                            ('FONT', (0, 0), (-1, -1), self.font_face),
                            ('FONTSIZE', (0, 0), (-1, -1), 8),
                            ('TEXTCOLOR', (0, 0), (-1, -1), (0.2, 0.2, 0.2)),
                            ('GRID', (0, 0), (-1, -2), 1, (0.7, 0.7, 0.7)),
                            ('GRID', (-1, -1), (-1, -1), 1, (0.7, 0.7, 0.7)),
                            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
                            ]+[('ALIGN',(k,0),(k,-1),'RIGHT') for k in righta])
                    tw, th, = table.wrapOn(canvas, 15 * cm, 19 * cm)
                    table.drawOn(canvas, 1 * cm, -18 * cm - th)
            canvas.showPage()
            canvas.save()
        return buffer.getvalue()



    styles = getSampleStyleSheet()  # дефолтовые стили
    # создаем объект документа с размером страницы A4
    doc = SimpleDocTemplate(response, pagesize=A4, title='Тест документа', author='CAV Inc')

    # doc.setFont('Helvetica', 12)

    buffer.append(Paragraph("The Platypus", styles['Heading1']))
    buffer.append(Paragraph('<font name="Helvetica">ЭТО СПАРТА !!!</font>', styles['Normal']))
    for i in range(500):
        buffer.append(Paragraph("Line in %s " % str(i), styles["Normal"]))
        buffer.append(Paragraph('<font name="Helvetica">Line in %s линия </font>' % str(i), styles["Normal"]))
    doc.build(buffer)


"""
