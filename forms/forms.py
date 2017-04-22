"""
    Библиотека для преобразования XLSX templates файлов в PDF для печати

"""
# openpyxl
from openpyxl import load_workbook
from openpyxl.utils.units import DEFAULT_ROW_HEIGHT, DEFAULT_COLUMN_WIDTH

# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.platypus import Table

# для шрифтов
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class Form(object):
    """ Класс для работы с шаблонами в формате Excel .
    Читает и подготавливает данные для экспорта в PDF.
    """
    # print(DEFAULT_ROW_HEIGHT, DEFAULT_COLUMN_WIDTH)
    PORTRAIT, LANDSCAPE = 'portrait', 'landscape'
    DEFAULT_CELL_HEIGHT = 11.0  # 15.0
    DEFAULT_CELL_WIDTH = 14.0  # 51.85
    DEFAULT_SHEET_ORIENTATION = PORTRAIT

    horizontal_align = {
        'right': 'RIGHT',
        'left': 'LEFT',
        'center': 'CENTER',
        None: 'None'
    }

    vertical_align = {
        'center': 'MIDDLE',
        'bottom': 'BOTTOM',
        'top': 'TOP',
        None: 'None'
    }

    cell_border = {
        'thin': 0.5,
        'medium': 2,
        'thick': 4,
    }

    ORIENTATION = {
        'landscape': landscape(A4),
        'portrait': portrait(A4),
    }

    # Допустимые части шаблона
    PARTS = {  # названия в шаблоне частей: #header
               'HEADER': 'header',
               'TABLE': 'table',
               'ROW': 'row',
               'TOTAL': 'total',
               'FOOTER': 'footer',
               }

    def __init__(self, output_file, context, file_prefix=u'document'):
        """ Initialise an object of the class Form

        :param context: context data for create the document form
        :type context: list

        :param file_prefix: file name prefix of the PDF file
        :type file_prefix: str

        :rtype: None

        """
        self.output_file = output_file
        self.context = context
        self.orientation = self.DEFAULT_SHEET_ORIENTATION
        self.workbook = ''
        self.worksheet = ''
        self.work_file = u'Empty'
        self.title = u'Form'
        self.width = 0  # Ширина XLSX страницы прочитанного шаблона
        self.height = 0  # Высота XLSX страницы прочитанного шаблона

        self.pdf_width = 0  # Ширина PDF страницы выбранной в качестве шаблона
        self.pdf_height = 0  # Высота PDF страницы выбранной в качестве шаблона
        self.pages = 0  # Текущая страница построенной формы или конечное значение
        # числа страниц итоговой формы

        self.rows = {}  # Словарь частей прочитанного шаблона со списком высот ячеек
        self.sizes = {}  # Словарь высот частей шаблона в px {'part': size}
        self.parts = []  # Список частей шаблона
        self._part = self.PARTS['HEADER']  # Текущая часть шаблона при чтении или построении формы (служебная)
        self._row = 0  # Текущая высота построенной формы шаблона в ячейках (служебная)
        self._height = 0  # Текущая высота построенной формы шаьлона в px (служебная)

        """ Настраиваем шрифт """
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        pdfmetrics.registerFont(TTFont('Arial', '../fonts/Arial.ttf'))
        # pdfmetrics.registerFont(TTFont('Arial Bold', '../fonts/Arial_Cyr.ttf'))

        """ Настраиваем стили и данные для report lab """
        self._data = {}  # Служебный словарь данных частей прочитанных из шаблона
        self._heights = {}  # Служебный словарь высот ячеек частей прочитанных из шаблона
        # self._widths = {}
        self._style = {}  # Служебный словарь стилей частей прочитанных из шаблона

        self.data = []  # Подготовленный список данных предназначенный для рендера формы
        self.heights = []  # Подготовленный список высот строк предназначенный для рендера формы
        self.widths = []  # Подготовленный список ширин ячеек  предназначенный для рендера формы
        self.style = []  # Подготовленный список стилей предназначенный для рендера формы

        self.init_style = [
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#e0e0e0')),  # для разработки
        ]

        self.logo = None

    def __str__(self):
        return self.output_file

    def __repr__(self):
        return u"<Form %s.%s>" % (self.title, self.work_file)

    # методы для сборки шаблона
    def _create(self):
        # создает начало шаблона
        self.document = canvas.Canvas(self.output_file, pagesize=self.orientation, bottomup=1)
        self.pdf_width, self.pdf_height = self.orientation
        self.pages = 0
        self._row = 0
        self._number = 0  # Номер обрабатываемой строки
        self._height = 0
        self.data = []
        self.heights = []
        self.style = []  # ????????????
        self.style.extend(self.init_style)  # добавляем в стиль каждой страницы
        return True

    def _extend(self, part, context):
        # функция присоединяет другую часть шаблона к существующему
        # if part == self.PARTS['ROW']:
        #    print(self._data[part][0])
        # print(self._data[part])

        # Обработка данных с добавлением значений в теги
        _data = []
        if context and part == self.PARTS['ROW']:
            self._number += 1
            for value in self._data[part][0]:  # Индекс 0 потому-что в списке находится 1 подсписок row(строка)
                if value[-2:] == '}}' and value[:2] == '{{':
                    # Вставляем значение из контекста документа
                    # На случай отсутствующих ключей обернём в try
                    try:
                        if value[2:-2] == 'number':
                            # Обработка номера строки
                            _data.append(str(self._number))
                        else:
                            _data.append(context[value[2:-2]])
                    except:
                        _data.append(value)  # Выводим не найденный тег
                        print('render(): Key Does not exist:', value[2:-2])
                else:
                    _data.append(value)
            self.data.extend([_data])  # Со строковой обработкой
        else:
            # print(self._data[part])
            self.data.extend(self._data[part])  # Если обработка не требуется как в строках

        # обработка стилей с добавлением смещения
        for style in self._style[part]:
            sx, sy = style[1]
            ex, ey = style[2]
            if len(style) == 3:
                # print(sx, sy, ex, ey)
                self.style.append(
                    (style[0], (sx, sy + self._row), (ex, ey + self._row))
                )
            elif len(style) == 4:
                self.style.append(
                    (style[0], (sx, sy + self._row), (ex, ey + self._row), style[3])
                )
            elif len(style) == 5:
                self.style.append(
                    (style[0], (sx, sy + self._row), (ex, ey + self._row), style[3], style[4])
                )
            else:
                print('Can\'t understand the style:', style)
                self.style.append(style)

        # print(self.style)
        # self.style.extend(self._style[part])
        self.heights.extend(self._heights[part])
        # Прибавляем row
        self._row += self.rows[part]
        self._height += self.sizes[part]
        return True

    def _make_page(self):
        # функция рисует подготовленный лист
        # Подготовка таблицы
        self.table = Table(self.data, colWidths=self.widths, rowHeights=self.heights, repeatRows=1)
        # Подготовка стилей
        self.table.setStyle(self.style)

        self.table_width, self.table_height = self.table.wrapOn(self.document, self.width, self.height)
        # print(table_height)
        self.table.drawOn(self.document, (self.pdf_width - self.width) / 2, self.height - self._height, mm)

        # Создаём страницу
        self.document.showPage()
        self.data = []
        self.heights = []
        self.style = self.init_style
        self.pages += 1
        self._row = 0
        self._height = 0
        return True

    def render(self):
        if self._data and self._heights and self.widths and self.orientation:
            if not self._create():
                print('Error: Can\'t create a PDF page')
                return False

            # Сначала шапку
            self._extend(self.PARTS['HEADER'], None)

            # Добавляем таблицу
            self._extend(self.PARTS['TABLE'], None)
            # добавляем строки

            _row = 0
            _rows = len(self.context['rows'])
            # Перебераем все строки из контекста
            for item in self.context['rows']:
                _row += 1
                _height = self._height + self.sizes[self.PARTS['TOTAL']]
                # print(self._height, self.sizes[self.PARTS['TOTAL']], self.height)
                if _height < self.height:
                    if _row == _rows:
                        # Ситуация 1: Если все строки вмещаются на странице и на последнюю переносятся только footer
                        # то мы последнюю строку отдадим на другую страницу
                        # Перенос на другую страницу
                        # Добавляем итоговою сроку
                        self._extend(self.PARTS['TOTAL'], None)
                        # Создаём страницу
                        self._make_page()
                        # Добавляем таблицу
                        self._extend(self.PARTS['TABLE'], None)
                    # Ситуация 2: Добавляем строку
                    # Добавляем строку
                    self._extend(self.PARTS['ROW'], item)
                else:
                    # Ситуация 2: Страница закончилась нужно переносить остальные строки на другой лист
                    # Добавляем итоговою сроку в каждом листе
                    self._extend(self.PARTS['TOTAL'], None)
                    # Далее строим новый лист
                    self._make_page()
                    # Рисуем шапку таблицы
                    # Добавляем таблицу
                    self._extend(self.PARTS['TABLE'], None)

            # Финализируем
            # Добавляем итоговою сроку в каждом листе
            self._extend(self.PARTS['TOTAL'], None)
            # Добавляем подвал
            self._extend(self.PARTS['FOOTER'], None)

            # Создаём страницу
            self._make_page()

            # Сохраняем документ
            self.document.save()

            # Информация для разработки
            # for part in self._data.keys():
            print(self.rows)

            print('Размеры PDF страницы(px): ', self.pdf_width, self.pdf_height)
            print('Размеры PDF страницы(mm): ', self.pdf_width / mm, self.pdf_height / mm)
            print('Размеры XLSX страницы(px): ', self.width, self.height)
            print('Размеры XLSX страницы(mm): ', self.width / mm, self.height / mm)

            # print(self.data)
            # print('width:', self.widths)
            # print('height:', self.heights)

            # my_cell = self.worksheet['AY6']
            # print('Ячейка:', my_cell.border.top.border_style)
            # print('Ячейки:', self.worksheet.merged_cells)
            # print('Объединены ячейки:', self.worksheet.merged_cell_ranges)

        else:
            print('Error: Load a form first!')
            return None
        return True

    def wrap(self, cell):
        """ Prepare a read's value from XLSX and wrapping value out of a context
            Функция подготовки прочитанных значений из XLSX и обработки значений из контекста
        """
        value = str(cell.value)
        br = chr(0x5c) + chr(0x6e)
        if value[0] == '#':
            #  Наименование части шаблона
            self._part = value[1:]
            self.parts.append(self._part)
            self._row = 0  # Каждую часть начинаем с нового отсчета
            print('найден маркер строки: %s' % value[1:])
            return ''
        elif value[-2:] == '}}' and value[:2] == '{{':
            # Вставляем значение из контекста документа
            try:
                # На случай отсутствующих ключей
                if self._part != self.PARTS['ROW']:
                    value = self.context[value[2:-2]]
                return value
            except:
                print('Key Does not exist:', value[2:-2])
            return value
        return value.replace(br, chr(10))  # Когда исправят в openpyxl убрать

    def load_xlsx(self, template_file_name, sheet_name=u'Sheet1'):
        """ Loading a template
            Загрузка шаблона

        :param template_file_name: Наименование файла
        :type template_file_name: str

        :param sheet_name: Наименование шаблона
        :type sheet_name: str

        :rtype: None (changed self: data, style, widths, heights)
        """
        self.work_file = template_file_name
        self.title = sheet_name
        self.workbook = load_workbook(filename=template_file_name)
        self.worksheet = self.workbook[sheet_name]
        # self.worksheet.cell.style.alignment.wrap_text = True
        """ Getting orientation of the page """
        self.orientation = self.ORIENTATION[self.worksheet.page_setup.orientation]

        """ Initialize of worksheet size and parts """
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
            value = row[0].value
            # читаем первый столбец и создаем словари для частей шаблона
            if value:
                value = str(value)[1:]
                self._part = value
                # добавляем словарь данных
                self._data.update({value: []})
                # добавляем словарь стилей
                self._style.update({value: []})
                # добавляем словарь высот
                self._heights.update({value: []})
                # добавляем словарь частей
                self.sizes.update({value: 0})
                # добавляем словарь строк в частях
                self.rows.update({value: 0})

            cell = self.worksheet.row_dimensions[row[0].row]
            # print(value)
            # print(cell.hidden) Скрытые ячейки
            if cell.hidden:
                # Скрытые строки
                self._heights[self._part].append(0)  # new
                # self.heights.append(0)
            elif cell.height:
                self._heights[self._part].append(cell.height)  # new
                # self.heights.append(cell.height)

                self.sizes[self._part] += cell.height  # new
                self.height += cell.height
            else:
                self._heights[self._part].append(self.DEFAULT_CELL_HEIGHT)  # new
                # self.heights.append(self.DEFAULT_CELL_HEIGHT)

                self.sizes[self._part] += self.DEFAULT_CELL_HEIGHT  # new
                self.height += self.DEFAULT_CELL_HEIGHT

        """ Getting values and styles of cells """
        #   Сформируем коллекцию из всех ячеек
        for row in self.worksheet.rows:
            data_cells = []
            for cell in row:
                if cell.value:
                    _wrap_cell = self.wrap(cell)
                    data_cells.append(_wrap_cell)
                    # размер шрифта
                    # print(cell.alignment.vertical)
                    # Размер шрифта
                    if _wrap_cell:
                        self._style[self._part].append(('FONTSIZE', (cell.col_idx - 1, self._row),
                                                        (cell.col_idx - 1, self._row), cell.font.sz))

                        # Горизонтальное выравнивание текста
                        if cell.alignment.horizontal:
                            self._style[self._part].append(('ALIGN', (cell.col_idx - 1, self._row),
                                                            (cell.col_idx - 1, self._row),
                                                            self.horizontal_align[cell.alignment.horizontal]))

                        # Вертикальное выравнивание текста
                        if cell.alignment.vertical:
                            self._style[self._part].append(('VALIGN', (cell.col_idx - 1, self._row),
                                                            (cell.col_idx - 1, self._row),
                                                            self.vertical_align[cell.alignment.vertical]))
                            # print('Толщина:', cell.border.top.border_style)
                else:
                    data_cells.append('')

                    # if cell.coordinate not in self.worksheet.merged_cells:    # работает, но очень медленно

                # Верхная граница
                if cell.border.top.border_style:
                    self._style[self._part].append(('LINEABOVE', (cell.col_idx - 1, self._row),
                                                    (cell.col_idx - 1, self._row),
                                                    self.cell_border[cell.border.top.border_style], colors.black))
                # Нижняя граница
                if cell.border.bottom.border_style:
                    self._style[self._part].append(('LINEBELOW', (cell.col_idx - 1, self._row),
                                                    (cell.col_idx - 1, self._row),
                                                    self.cell_border[cell.border.bottom.border_style], colors.black))
                # Левая граница
                if cell.border.left.border_style:
                    self._style[self._part].append(('LINEBEFORE', (cell.col_idx - 1, self._row),
                                                    (cell.col_idx - 1, self._row),
                                                    self.cell_border[cell.border.left.border_style], colors.black))
                # Правая граница
                if cell.border.right.border_style:
                    self._style[self._part].append(('LINEAFTER', (cell.col_idx - 1, self._row),
                                                    (cell.col_idx - 1, self._row),
                                                    self.cell_border[cell.border.right.border_style], colors.black))

            # в новом формате
            self._data[self._part].append(data_cells)
            self.rows[self._part] += 1
            self._row += 1

            # добавляем как в первом варианте
            # self.data.append(data_cells)

        """ Формируем стили для объединённых ячеек """
        """ Make styles for merged cells """

        # for cell in self.worksheet['AY7:BF8']:
        #            print('Ячейка: ', cell, 'Border-')


        ranges = []
        self._row = 0
        # Список объединений переведенных в цифровое обозначение
        for merged_range in self.worksheet.merged_cell_ranges:
            cell_range = merged_range.split(':', 2)
            cell_start = self.worksheet[cell_range[0]]  # used the new method: worksheet['A1']
            cell_end = self.worksheet[cell_range[1]]
            # вычисляем начало части шаблона в которую входит объединение

            _start_row = cell_start.row - 1  # Запомним начало
            _end_row = cell_end.row - 1 - _start_row  # Запомним разницу между верхней и нижней
            for self._part in self.parts:  # Вычисляем часть в которой происходит действие
                if _start_row - self.rows[self._part] < 0:
                    break  # Вычислили первую и часть в которой она находится в шаблоне
                else:
                    _start_row -= self.rows[self._part]
            _end_row += _start_row  # Нижная будет разница + верхняя

            # Создаем список стилей
            ranges.append([self._part, cell_start.col_idx - 1, _start_row, cell_end.col_idx - 1, _end_row])

            # Верхная граница
            if cell_start.border.top.border_style:
                self._style[self._part].append(('LINEABOVE',
                                                (cell_start.col_idx - 1, _start_row),
                                                (cell_end.col_idx - 1, _start_row),
                                                self.cell_border[cell_start.border.top.border_style], colors.black))
            # Левая граница
            if cell_start.border.left.border_style:
                self._style[self._part].append(('LINEBEFORE',
                                                (cell_start.col_idx - 1, _start_row),
                                                (cell_start.col_idx - 1, _end_row),
                                                self.cell_border[cell_start.border.left.border_style], colors.black))
            # Нижняя граница
            if cell_start.border.bottom.border_style:
                self._style[self._part].append(('LINEBELOW',
                                                (cell_start.col_idx - 1, _end_row),
                                                (cell_end.col_idx - 1, _end_row),
                                                self.cell_border[cell_start.border.bottom.border_style], colors.black))
            # Правая граница
            if cell_end.border.right.border_style:
                self._style[self._part].append(('LINEAFTER',
                                                (cell_end.col_idx - 1, _start_row),
                                                (cell_end.col_idx - 1, _end_row),
                                                self.cell_border[cell_end.border.right.border_style], colors.black))

        # После вычисления обавляем добавляем стили в нужные части
        for span in ranges:
            self._style[span[0]].append((
                'SPAN', (span[1], span[2]), (span[3], span[4])
            ))
        return True
