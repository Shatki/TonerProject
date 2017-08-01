"""
Библиотека для преобразования XLSX templates файлов в PDF для печати

Created on 12.03.2017
Changed on 05.05.2017
@author: Dmitriy Seliverstov <shatki@mail.ru>
"""
# benchmark
import time
# load django settings
from django.conf import settings
# openpyxl
from openpyxl import load_workbook
# reportlab
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4, portrait, landscape
from reportlab.platypus import Table
# fonts
from reportlab.pdfbase import pdfmetrics
from  reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
# number to string writing of number library
from .num2text import num2text, decimal2text, int_units, exp_units


class Form(object):
    """ Class for generation a PDF from XLSX template with data and tags
    Класс для работы с шаблонами в формате Excel .
    Читает и подготавливает данные для экспорта в PDF.
    """
    # print(DEFAULT_ROW_HEIGHT, DEFAULT_COLUMN_WIDTH)
    PORTRAIT, LANDSCAPE = 'portrait', 'landscape'
    DEFAULT_CELL_HEIGHT = 11.0  # 15.0
    DEFAULT_CELL_WIDTH = 14.0  # 51.85
    DEFAULT_SHEET_ORIENTATION = PORTRAIT
    FONT_NAME = 'Arial'
    CONTEXT_ROWS_DATA_NAME = 'rows'

    ORIENTATION = {
        LANDSCAPE: landscape(A4),
        PORTRAIT: portrait(A4),
    }

    ''' openpyxl to report lab relation's constants '''
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

    # Template parts
    PARTS = (
        'HEADER',
        'TABLE',
        'ROW',
        'TOTAL',
        'FOOTER',
    )

    # Template parts name converter
    PART = dict(
        # названия в шаблоне частей: #header
        HEADER='header',
        TABLE='table',
        ROW='row',
        TOTAL='total',
        FOOTER='footer',
    )

    # Template context
    CONTEXT = {
        'pages': 1,  # Текущая страница построенной формы или конечное значение
        'numbers': 0,
        'total': {},
    }

    # Template short access's names
    HEADER = PART['HEADER']
    TABLE = PART['TABLE']
    ROW = PART['ROW']
    TOTAL = PART['TOTAL']
    FOOTER = PART['FOOTER']

    def __init__(self, output_file, context, file_prefix=u'document'):
        """ Initialise an object of the class Form

        :param context: context data for create the document form
        :type context: list

        :param file_prefix: file name prefix of the PDF file
        :type file_prefix: str

        :rtype: None

        """
        self.template_name = ''
        self.output_file = output_file
        self.context = context
        self.orientation = self.DEFAULT_SHEET_ORIENTATION
        self.workbook = ''  # Название файла
        self.worksheet = ''
        self.work_file = u'NotLoad'
        self.title = u'None'
        self.width = 0  # Ширина XLSX страницы прочитанного шаблона
        self.height = 0  # Высота XLSX страницы прочитанного шаблона

        self.pdf_width = 0  #Ширина PDF страницы выбранной в качестве шаблона
        self.pdf_height = 0  # Высота PDF страницы выбранной в качестве шаблона
        self.rows = {}  # Словарь частей прочитанного шаблона со списком высот ячеек
        self.sizes = {}  # Словарь высот частей шаблона в px {'part': size}
        self.parts = []  # Список частей шаблона
        self._part = self.HEADER  # Текущая часть шаблона при чтении или построении формы (служебная)
        self._row = 0  # Текущая высота построенной формы шаблона в ячейках (служебная)
        self._height = 0  # Текущая высота построенной формы шаьлона в px (служебная)
        self.tags = {}  # Словарь всех тегов в шаблоне

        """ Setup font of the output PDF """
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        pdfmetrics.registerFont(TTFont(self.FONT_NAME, '../fonts/Arial.ttf'))
        # pdfmetrics.registerFont(TTFont('Arial Bold', '../fonts/Arial_Cyr.ttf'))

        """ Setup styles, date and geometry of template for render to report lab """
        self._data = {}  # Служебный словарь данных частей прочитанных из шаблона
        self._heights = {}  # Служебный словарь высот ячеек частей прочитанных из шаблона
        self._style = {}  # Служебный словарь стилей частей прочитанных из шаблона
        self.data = []  # Подготовленный список данных предназначенный для рендера формы
        self.heights = []  # Подготовленный список высот строк предназначенный для рендера формы
        self.widths = []  # Подготовленный список ширин ячеек  предназначенный для рендера формы
        self.style = []  # Подготовленный список стилей предназначенный для рендера формы

        """ Init style for render template """
        self.init_style = [
            ('FONTNAME', (0, 0), (-1, -1), self.FONT_NAME),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]

        if settings.DEBUG:
            self.init_style += ('GRID', (0, 0), (-1, -1), 0.25, colors.HexColor('#e0e0e0')),  #для разработки

        self.logo = None

    def __str__(self):
        if self.template_name:
            return u"Form: [<Template ""%s"">, %s]" % (self.work_file.split('/')[-1], self.template_name)
        else:
            return u'The template isn''t loaded'

    def __repr__(self):
        if self.template_name:
            return u"Form: [<Template ""%s"">, %s]" % (self.work_file.split('/')[-1], self.template_name)
        else:
            return u'The template isn''t loaded'

    def _hyphen(self, part, string, tag_name):
        """Making a multi line string from string value and correcting lenght of the string
        :param string: string value
        :param tag_name: tag name of value for getting string from context
        :return string: a reformat string
        """
        try:
            # Алгоритм обработки строки из однострочной в многострочную согласно вычисленным данным
            _w, _h, _fs = self.tags[part][tag_name]
            _new_val = ''
            _line = 0
            _space = stringWidth(' ', self.FONT_NAME, _fs)
            _w -= _space  # Убавим максимальную ширину на пробел чтоб не попасть точно на границы
            for _val in string.split(' '):
                _len_val = stringWidth(_val, self.FONT_NAME, _fs)
                # расставляем переноcы
                if _line + _len_val > _w:
                    # Этот способ ограничения количества строк не учитывает межстрочные интервалы
                    _h -= _fs
                    if _h < _fs:
                        # Ограничение максимального количества строк
                        break
                    _new_val += '\n'
                    _new_val += _val
                    _line = stringWidth(_val, self.FONT_NAME, _fs)
                else:
                    if _new_val:
                        _new_val += ' ' + _val
                        _line += _len_val + _space
                    else:
                        _new_val += _val
                        _line += _len_val
            string = _new_val
        except:
            if not tag_name.split('.')[0] in self.CONTEXT['total']:
                # Если тег даже не из внутреннего контекста 'CONTEXT'
                if settings.DEBUG:
                    print('_hyphen: Не найден тег: {{%s}} в части %s' % (tag_name, part))
        return string

    # методы для сборки шаблона
    def _create(self):
        # создает начало шаблона
        self.document = canvas.Canvas(self.output_file, pagesize=self.orientation, bottomup=1)
        self.pdf_width, self.pdf_height = self.orientation
        self.CONTEXT['pages'] = 1
        self._row = 0
        self.CONTEXT['numbers'] = 0  # Номер обрабатываемой строки
        self._height = 0
        self.data = []
        self.heights = []
        self.style = []  # ????????????
        self.style.extend(self.init_style)  # добавляем в стиль каждой страницы
        return True

    def _extend(self, part, _context):
        """ This method needs for build the output form.
            Add a part of template to the exist output form

        :param part: name of template part
        :param _context: the context with data to render the form
        :return : boolean: result of method's action
        """
        # функция присоединяет другую часть шаблона к существующему
        if not _context:
            _context = self.context

        # Обработка данных с добавлением значений в теги
        _data = []
        # Тут только строки ROW
        if _context and part == self.ROW:
            self.CONTEXT['numbers'] += 1
            for value in self._data[part][0]:  # Индекс 0 потому-что в списке находится 1 подсписок row(строка)
                if value[-2:] == '}}' and value[:2] == '{{':
                    tag = value[2:-2]
                    # Вставляем значение из контекста документа
                    # На случай отсутствующих ключей обернём в try
                    try:
                        if tag == 'number':
                            # Обработка номера строки
                            _data.append(str(self.CONTEXT['numbers']))
                        else:
                            # Заменяем тег на значение из контекста в строке
                            # Используем функуию преобразования строки по "габаритам"
                            _data.append(self._hyphen(part, str(_context[tag]), tag))
                            # Прибавим счетчики если такие ключи есть в CONTEXT
                            if tag in self.CONTEXT['total']:
                                self.CONTEXT['total'][tag][0] += float(_context[tag])
                                self.CONTEXT['total'][tag][self.CONTEXT['pages']] += float(_context[tag])
                    except:
                        if settings.DEBUG:
                            _data.append(value)  # Выводим не найденный тег
                        else:
                            _data.append('')  # Выводим не найденный тег
                        print('_extend(): Ошибка шаблона или неверные данные получены в контексте по ключу: %s' % tag)
                else:
                    _data.append(value)
            self.data.extend([_data])  # Со строковой обработкой
        else:
            # Обработка части данных с заменой тегов на значения из посчитанных данных
            # Данные многостройные
            # Все остальные части шаблона
            for data_row in self._data[part]:
                data_cells = []
                for val in data_row:
                    val = str(val)
                    # Если попался тег
                    if val[-2:] == '}}' and val[:2] == '{{':
                        # Вставляем значение из контекста документа
                        tags = val[2:-2]
                        try:
                            # Поддержка каскадных тегов value.tag1.tag2
                            values = tags.split('.')
                            # Есть теги...
                            if len(values) > 1:
                                _val = ''
                                for tag in values:
                                    # print(tags, tag)
                                    # Первым идет ключ - пропускаем
                                    if tag != values[0]:
                                        # Каскады тегов - чем выше тут в ветке if, тем больше приоритет тега
                                        # totalpage  - предварительный итог по странице
                                        if tag == 'totalpage':
                                            # Берем значение из контекста, а данные по индексу страницы
                                            _val = self.CONTEXT['total'][values[0]][self.CONTEXT['pages']]
                                        # total
                                        elif tag == 'total':
                                            # Берем специально подготовленное значение из контекста: индекс 0
                                            _val = self.CONTEXT['total'][values[0]][0]
                                        # textcost  - перевод цифрового значения стоимости в
                                        elif tag == 'textcost':
                                            # Берем значение из внутреннего или внешнего контекста по ключу
                                            if _val:
                                                _val = decimal2text(_val, 2, int_units, exp_units)
                                            else:
                                                _val = decimal2text(self.CONTEXT[values[0]], 2, int_units, exp_units)
                                            break
                                        # textvalue -  перевод цифрового значяения в строковой
                                        elif tag == 'textvalue':
                                            # Берем значение из внутреннего или внешнего контекста по ключу
                                            if _val:
                                                _val = num2text(_val)
                                            else:
                                                _val = num2text(self.CONTEXT[values[0]])
                                            break
                                        else:
                                            # Тег не найден
                                            if settings.DEBUG:
                                                print('_extend: Cannot find tag:', tag)
                            # После обработки добавим значение
                            # self._hyphen(part, _context[value], val)
                            # print(part, val, value)
                            else:
                                # Тег не каскадный
                                # Обработка тегов из всех частей кроме ROW, заменяем значением из контекста
                                _val = str(self.context[tags])
                            # print(val, value)
                            data_cells.append(self._hyphen(part, _val, tags))  # Форматируем строчку по размеру
                        except:
                            if settings.DEBUG:
                                print('_extend: Данные тега {{%s}} не обнаружены' % tags)
                                # Просто выводим пустое значение вмето тега value
                                data_cells.append(val)
                            else:
                                data_cells.append('')
                    else:
                        if settings.DEBUG:
                            data_cells.append(val)
                        else:
                            data_cells.append('')
                _data.append(data_cells)

            self.data.extend(_data)  # Если обработка не требуется как в строках
            # print(self._data[part])
            # self.data.extend(self._data[part])  # Если обработка не требуется как в строках

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
                if settings.DEBUG:
                    print('_extend: Can\'t recognize the style:', style)
                    # self.style.append(style)

        # print(self.style)
        # self.style.extend(self._style[part])
        self.heights.extend(self._heights[part])
        # Прибавляем row
        self._row += self.rows[part]
        self._height += self.sizes[part]
        return True

    def _make_page(self):
        """ Make a page of the form used the data and 'reportlab' library
        :return: boolean: result of method's action
        """
        try:
            # функция рисует подготовленный лист
            # Подготовка таблицы
            self.table = Table(self.data, colWidths=self.widths, rowHeights=self.heights, repeatRows=1)
            # Подготовка стилей
            self.table.setStyle(self.style)

            # w, h = self.table.wrap(self.width, self.height)
            self.table_width, self.table_height = self.table.wrapOn(self.document, self.width, self.height)
            # print(table_height)
            self.table.drawOn(self.document, (self.pdf_width - self.width) / 2,
                              self.height - self._height + self.DEFAULT_CELL_HEIGHT, mm)

            # Создаём страницу
            self.document.showPage()
            self.data = []
            self.heights = []
            self.style = self.init_style
            self.CONTEXT['pages'] += 1
            # Добавим контекст итогов, будет на одно значение больше из-за расположения)
            for tag in self.CONTEXT['total']:
                self.CONTEXT['total'][tag].append(0)
            self._row = 0
            self._height = 0
        except:
            print('_make_page: Cannot make a page with received data. Check the template')
            return False
        return True

    def _wrap(self, cell):
        """ Prepare a read's value from XLSX and wrapping value out of a context
            Функция обработки прочитанных значений из XLSX, кроме тегов
        """
        value = str(cell.value)
        br = chr(0x5c)
        if value[-12:] == '.totalpage}}' and value[:2] == '{{' and self._part == self.TOTAL:
            # Заполнение коллекции ключей в CONTEXT
            try:
                # Делаем запись в контекст и добавляем 0 - общий итог и 0 по первой странице
                self.CONTEXT['total'].update({value[2:-2].split('.')[0]: [0, 0]})
            except:
                print('_wrap: Не могу добавить {total} ключ %s' % value[2:-2])
        elif value[0] == '#':
            self._part = value[1:]
            self._row = 0  # Каждую часть начинаем с нового отсчета
            return ''
        return value.replace(br, chr(10))  # Когда исправят в openpyxl убрать

    def render(self):
        """
        Render the loaded template with class's load methods
        :return: boolean: result of method's action
        """
        _t = time.time()
        if self._data and self._heights and self.widths and self.orientation:
            if not self._create():
                print('Error: Can\'t create a PDF page')
                return False

            for self._part in self.PARTS:
                if self.PART[self._part] == self.ROW:
                    _row = 0
                    _rows = len(self.context[self.CONTEXT_ROWS_DATA_NAME])
                    # Перебераем все строки из контекста
                    for item in self.context[self.CONTEXT_ROWS_DATA_NAME]:
                        _row += 1
                        _height = self._height + self.sizes[self.TOTAL]
                        if _height < self.height:
                            if _row == _rows and _rows > 1:
                                # Ситуация 1: Если все строки вмещаются на странице и на последнюю
                                # переносятся только footer то мы последнюю строку отдадим на другую страницу
                                # Перенос на другую страницу
                                # Добавляем итоговою сроку
                                self._extend(self.TOTAL, self.context)
                                # Создаём страницу
                                self._make_page()
                                # Добавляем таблицу
                                self._extend(self.TABLE, self.context)
                            # Ситуация 2: Добавляем строку
                            # Добавляем строку
                            self._extend(self.ROW, item)
                        else:
                            # Ситуация 3: Страница закончилась нужно переносить остальные строки на другой лист
                            # Добавляем итоговою сроку в каждом листе
                            self._extend(self.TOTAL, self.context)
                            # Далее строим новый лист
                            self._make_page()
                            # Рисуем шапку таблицы
                            # Добавляем таблицу
                            self._extend(self.TABLE, self.context)
                else:
                    # Рисуем часть шаблона отличную от ROW
                    self._extend(self.PART[self._part], self.context)

            # Рисуем последнюю страницу
            self._make_page()

            # Сохраняем документ
            self.document.save()

            if settings.DEBUG:
                print('Time of rendering template: ', time.time() - _t)

                # Информация для разработки
                # for part in self._data.keys():
                # print(self.CONTEXT['total'])
                # print(self.worksheet.merged_cell_ranges)
                # print(self.height, decimal2text(self.height, 2, int_units, exp_units))

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

    def load_template(self, template_file_name, sheet_name=''):
        """ Loading a template
            Загрузка шаблона

        :param template_file_name: Наименование файла
        :type template_file_name: str

        :param sheet_name: Наименование шаблона
        :type sheet_name: str

        :rtype: None (changed self: data, style, widths, heights)
        """
        _t = time.time()
        try:
            self.work_file = template_file_name
            self.title = sheet_name
            self.workbook = load_workbook(filename=template_file_name)
            if sheet_name:
                self.worksheet = self.workbook[sheet_name]
            else:
                self.worksheet = self.workbook.active
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
                # формируем геометрию шаблона по первому столбцу
                if value:
                    value = str(value)[1:]
                    #  Наименование части шаблона
                    self.parts.append(value)
                    if settings.DEBUG:
                        print('load_xlsx: найден маркер раздела шаблона: %s' % value)
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
                    # добавляем словарь пространства тегов
                    self.tags.update({value: {}})

                # добавляем размеры частей в строках
                self.rows[self._part] += 1

                cell = self.worksheet.row_dimensions[row[0].row]
                # print(value)
                # print(cell.hidden) Скрытые ячейки
                if cell.hidden:
                    # Скрытые строки
                    self._heights[self._part].append(0)  # new
                elif cell.height:
                    self._heights[self._part].append(cell.height)  # new
                    self.sizes[self._part] += cell.height  # new
                    self.height += cell.height
                else:
                    self._heights[self._part].append(self.DEFAULT_CELL_HEIGHT)  # new
                    self.sizes[self._part] += self.DEFAULT_CELL_HEIGHT  # new
                    self.height += self.DEFAULT_CELL_HEIGHT

            """ Формируем стили для объединённых ячеек """
            """ Make styles for merged cells """
            # list диапазонов объединенных ячеек
            ranges = []
            # list ячеек исключения формирования одиночных стилей ячеек
            cell_except = []
            self._row = 0
            # Список объединений переведенных в цифровое обозначение
            for merged_range in self.worksheet.merged_cell_ranges:
                cell_range = merged_range.split(':', 2)
                cell_start = self.worksheet[cell_range[0]]  # used the new method: worksheet['A1']
                cell_end = self.worksheet[cell_range[1]]
                # Добавим первую ячейку в исключающий list
                cell_except += [cell_start.coordinate]

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

                # Тут мы собираем все теги в один словарь для формирования справочника
                # Это необходимо для форматирования значений из контекста подставляемые в теги
                value = str(cell_start.value)
                _w, _h = 0, 0
                if value[-2:] == '}}' and value[:2] == '{{':
                    # Вычисление ширины окна тега
                    for idx in range(cell_start.col_idx - 1, cell_end.col_idx):
                        _w += self.widths[idx]
                    for idx in range(_start_row, _end_row + 1):
                        # print(self._part, idx)
                        # print(self._heights[self._part][idx])
                        _h += self._heights[self._part][idx]

                    # Добавляем в словарь именованную ширину и высоту окна тега, а также координаты для
                    # отличия одноименных тегов в местах расположения в шаблоне
                    # Значения в словаре вида {xx$yy$tag_name: (width, height)}
                    self.tags[self._part].update(
                        {value[2:-2]: (_w, _h, cell_start.font.sz)}
                    )

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
                                                    self.cell_border[cell_start.border.left.border_style],
                                                    colors.black))
                # Нижняя граница
                if cell_start.border.bottom.border_style:
                    self._style[self._part].append(('LINEBELOW',
                                                    (cell_start.col_idx - 1, _end_row),
                                                    (cell_end.col_idx - 1, _end_row),
                                                    self.cell_border[cell_start.border.bottom.border_style],
                                                    colors.black))
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

            """ Getting values and styles of cells """
            #   Сформируем коллекцию из всех ячеек
            for row in self.worksheet.rows:
                data_cells = []
                for cell in row:
                    if cell.value:
                        _wrap_cell = self._wrap(cell)
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

                    if cell.coordinate in cell_except:  # исключаем стили в ячейках с объединением
                        cell_except.remove(cell.coordinate)
                    else:
                        # Верхная граница
                        if cell.border.top.border_style:
                            self._style[self._part].append(('LINEABOVE', (cell.col_idx - 1, self._row),
                                                            (cell.col_idx - 1, self._row),
                                                            self.cell_border[cell.border.top.border_style],
                                                            colors.black))
                        # Нижняя граница
                        if cell.border.bottom.border_style:
                            self._style[self._part].append(('LINEBELOW', (cell.col_idx - 1, self._row),
                                                            (cell.col_idx - 1, self._row),
                                                            self.cell_border[cell.border.bottom.border_style],
                                                            colors.black))
                        # Левая граница
                        if cell.border.left.border_style:
                            self._style[self._part].append(('LINEBEFORE', (cell.col_idx - 1, self._row),
                                                            (cell.col_idx - 1, self._row),
                                                            self.cell_border[cell.border.left.border_style],
                                                            colors.black))
                        # Правая граница
                        if cell.border.right.border_style:
                            self._style[self._part].append(('LINEAFTER', (cell.col_idx - 1, self._row),
                                                            (cell.col_idx - 1, self._row),
                                                            self.cell_border[cell.border.right.border_style],
                                                            colors.black))
                # добавляем list строки в list шаблона
                self._data[self._part].append(data_cells)
                self._row += 1
                self.template_name = self.workbook.active
        except:
            print('Forms: Template did not load. Check the template for mistakes')
            return False
        if settings.DEBUG:
            print('Time of loading template: ', time.time() - _t)
        return True
