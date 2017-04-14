#!/usr/local/bin/python

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, landscape, A5
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("test_report_lab.pdf", pagesize=A5, rightMargin=30, leftMargin=30, topMargin=30,
                        bottomMargin=18)
# doc.pagesize = landscape(A4)
elements = []

data = [
    ["Letter", "Number", "Stuff", "Long stuff that should be wrapped"],
    ["A", "01", "ABCD", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"],
    ["B", "02", "CDEF", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"],
    ["C", "03", "SDFSDF", "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"],
    ["D", "04", "SDFSDF", "DDDDDDDDDDDDDDDDDDDDDDDD DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"],
    ["E", "05", "GHJGHJGHJ", "EEEEEEEEEEEEEE EEEEEEEEEEEEEEEEE EEEEEEEEEEEEEEEEEEEE"],
]

# TODO: Get this line right instead of just copying it from the docs
style = TableStyle([('ALIGN', (1, 1), (-2, -2), 'RIGHT'),
                    ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
                    ('VALIGN', (0, 0), (0, -1), 'TOP'),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.blue),
                    ('ALIGN', (0, -1), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, -1), (-1, -1), 'MIDDLE'),
                    ('TEXTCOLOR', (0, -1), (-1, -1), colors.green),
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ])

# Configure style and word wrap
s = getSampleStyleSheet()
s = s["BodyText"]
s.wordWrap = 'CJK'
data2 = [[Paragraph(cell, s) for cell in row] for row in data]
t = Table(data2)
t.setStyle(style)

# Send the data and build the file
elements.append(t)
doc.build(elements)

"""

    Catalog = []
    styles = getSampleStyleSheet()
    style = styles['Normal']
    styles.add(ParagraphStyle(name='Justify', wordWrap=True, fontSize=12))
    header = Paragraph(u'%s' % '''As fffddddfffff   dddddddddd dffffffffffffff df  ddddddfdkjfkdjfkjdkfjkdjfdfkjkdf''', styles['Justify'])
    Catalog.append(header)
    row1 = [['dsddfffffffdghghh'],
            [header]]
    t = Table(row1, 1*[7*cm], 2*[4*cm])
    t.setStyle(TableStyle(
            [('GRID', (0,0), (1,-1), 1, colors.black),
             ('LINEBELOW', (0,0), (-1,0), 1, colors.white),
             ('BACKGROUND', (0, 0), (-1, 0), colors.pink)]))
    Catalog.append(t)
    doc.build(Catalog)



    table = Table(data, colWidths=widths, rowHeights=heights, repeatRows=1)
    table.setStyle(style)

    table_width, table_height = table.wrapOn(document, width, height)

    document.setFont('Arial', 7)
    # canvas.rect(x, y, width, height, stroke=1, fill=0)
    document.setLineWidth(1)
    # document.rect(1*mm, 1*mm, 50*mm, 50*mm)


    # print(table_height)
    table.drawOn(document, *coord(10.1, 96.1 + (table_height / mm), mm))

    # Верхнее поле
    document.setFont('Arial', 6)
    document.drawString(x(179.2), y(11.6),
                        u'Унифицированная форма № ТОРГ-12. Утверждена постановлением Госкомстата России от 25.12.98 № 132')


"""
