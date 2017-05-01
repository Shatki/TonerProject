from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', '../fonts/Arial.ttf'))
_w, _h, _fs = 566.6, 22.5, 8.0

string = 'I understand (I think). Please explain how the wanted value is specified. Is it a (the only) leaf in the tree which fits a certain condition? What is this condition? To perform a search in a tree you can use breadth-search or depth-search or a more custom-tailored variant. But I need to know more about the situation you are in to give qualified advice. '

_new_val = ''
_line = 0

for _val in string.split(' '):
    _len_val = stringWidth(_val + ' ', 'Arial', _fs)
    # print(_get_string_width(_new_val))
    # расставляем переноcы
    print(_line)
    if _line + _len_val > _w:
        _h -= _fs
        print(_new_val, stringWidth(_new_val, 'Arial', _fs))
        if _h < _fs:
            # Ограничение максимального количества строк
            break
        _new_val += '\n'
        _new_val += _val
        _line = 0
    else:
        if _new_val:
            _new_val += ' ' + _val
            _line += _len_val + 1
        else:
            _new_val += _val
            _line += _len_val

print(_new_val, stringWidth(_new_val, 'Arial', _fs))
