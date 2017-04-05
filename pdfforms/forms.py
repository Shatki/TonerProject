"""
    Библиотека для преобразования XLSX templates файлов в PDF для печати

"""
import os
from TonerProject.settings import BASE_DIR, STATIC_URL, DOCUMENT_DIR
from datetime import datetime

# openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Border, Side, PatternFill, Font, GradientFill, Alignment
from openpyxl.worksheet import dimensions

# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
# для шрифтов
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class Form(object):
    def __init__(self, form_file, form_name, form_data, file_prefix=u'document'):
        self.pdf_file_name = file_prefix + datetime.now().strftime('-%Y-%m-%d-%H-%M-%S') + '.pdf'
        self.pdf_file = os.path.join(BASE_DIR, 'static', 'documents', self.pdf_file_name)
        self.xlsx = XLSX()
        data, style, widths, heights = self.xlsx.load_form(form_file, form_name)
        self.pdf = PDF(self.pdf_file, landscape(A4))
        # buffer = StringIO()
        self.pdf.add_table(data, style, widths, heights)
        self.pdf.render()


class XLSX(object):
    PORTRAIT, LANDSCAPE = 'portrait', 'landscape'
    DEFAULT_CELL_HEIGHT = 11.0
    DEFAULT_CELL_WIDTH = 14.0
    DEFAULT_SHEET_ORIENTATION = PORTRAIT

    def __init__(self):
        self.orientation = self.DEFAULT_SHEET_ORIENTATION
        self.workbook = ''
        self.worksheet = ''

        self.data = []
        self.style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
        ])
        self.heights = []
        self.widths = []
        self.width = 0
        self.height = 0

    def load_form(self, filename, sheetname=u'Sheet1'):
        """ Читаем заготовку """
        self.workbook = load_workbook(filename=filename)
        self.worksheet = self.workbook[sheetname]
        self.orientation = self.worksheet.page_setup.orientation

        """ Получаем размеры ячееек """
        first_row = self.worksheet[1]
        for cell in first_row:
            cel = self.worksheet.column_dimensions[cell.column]
            # print(cell.col_idx)
            if cel.hidden:
                # Скрытые столбцы
                self.widths.append(0)
            elif cel.width:
                self.widths.append(cel.width * 5.2)
                self.width += cel.width * 5.2
            else:
                self.widths.append(self.DEFAULT_CELL_WIDTH)
                self.width += self.DEFAULT_CELL_WIDTH

        for row in self.worksheet.rows:
            cell = self.worksheet.row_dimensions[row[0].row]
            # print(cell.hidden) Скрытые ячейки
            if cell.hidden:
                # Скрытые строки
                self.heights.append(0)
            elif cell.height:
                self.heights.append(cell.height)
                self.height += cell.height
            else:
                self.heights.append(self.DEFAULT_CELL_HEIGHT)
                self.height += self.DEFAULT_CELL_HEIGHT

        """ Получаем значения из ячееек """
        for row in self.worksheet.rows:
            data_cells = []
            for cell in row:
                if cell.value:
                    data_cells.append(cell.value)
                else:
                    data_cells.append('')
                    # widths.append(dimensions(cell).)
                    # print(cell.font.sz) размер шрифта
            self.data.append(data_cells)
        """ Формируем дополнительные стили """

        print(self.data)
        # print('width:', self.widths)
        # print('height:', self.heights)
        print(self.worksheet.max_column, self.worksheet.max_row)

        my_cell = self.worksheet['AY6']
        print('Ячейка:', my_cell.border.top.border_style)
        # print('Ячейки:', self.worksheet.merged_cells)
        # print('Объединены ячейки:', self.worksheet.merged_cell_ranges)

        print('Размеры XLS страницы: ', self.width, self.height)
        return self.data, self.style, self.widths, self.heights


class PDF(object):
    def __init__(self, filename, page_size=portrait(A4)):
        self.logo = None
        self.width, self.height = page_size
        self.document = canvas.Canvas(filename, pagesize=landscape(A4), bottomup=1)
        """ Настраиваем шрифт """
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        pdfmetrics.registerFont(TTFont('Arial', '../fonts/Arial_Cyr.ttf'))

        # Информация
        print('Размеры PDF страницы: ', self.width, self.height)
        print('Размеры PDF страницы(mm): ', self.width / mm, self.height / mm)

    def add_table(self, data, style, widths, heights):
        self.table = Table(data, colWidths=widths, rowHeights=heights, repeatRows=1)
        self.table.setStyle(style)
        self.table_width, self.table_height = self.table.wrapOn(self.document, self.width, self.height)
        self.table_width, self.table_height = self.table.wrapOn(self.document, self.width, self.height)
        # print(table_height)
        self.table.drawOn(self.document, 0, 0, mm)

    def render(self):
        self.document.showPage()
        self.document.save()

    """
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
