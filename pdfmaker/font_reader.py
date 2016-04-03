#!/usr/bin/python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools import ttLib
from glob import glob


def registerFonts():
    rootDir = "fonts"

    for fontLoc in glob(rootDir + "/*.ttf"):
        ttFont = ttLib.TTFont(fontLoc)
        try:
            fontName = shortName(ttFont)
            #print "Registering {} from {}".format(fontName[0],fontLoc)
            pdfmetrics.registerFont(TTFont(fontName[0],fontLoc))
        except IOError as e:
            print e
    print "Registered Fonts"


FONT_SPECIFIER_NAME_ID = 4
FONT_SPECIFIER_FAMILY_ID = 1


def shortName(font):
    """Get the short name from the font's names table"""
    name = ""
    family = ""
    for record in font['name'].names:
        if b'\x00' in record.string:
            name_str = record.string.decode('utf-16-be')
        else:
            name_str = record.string.decode('utf-8')
        if record.nameID == FONT_SPECIFIER_NAME_ID and not name:
            name = name_str
        elif record.nameID == FONT_SPECIFIER_FAMILY_ID and not family:
            family = name_str
        if name and family: break
    return [name, family]
