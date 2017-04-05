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
