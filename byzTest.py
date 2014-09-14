# -*- coding: utf-8 -*-
# byzTest.py

import neume_dict

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

class Cursor:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

# Register fonts
fontsDir = "C:\\Windows\\Fonts\\"
psalticaTTF = fontsDir + "EZ Psaltica.TTF"
oxeiaTTF    = fontsDir + "EZ Oxeia.ttf"
pdfmetrics.registerFont(TTFont("EZPsaltica",psalticaTTF,asciiReadable=True))
pdfmetrics.registerFont(TTFont("EZOxeia",oxeiaTTF))

# Neumes
LIHC = u'O S ! ! 1 1 \' ! ! ; " ! s \ 0 ! s 1 w ! A | v V J '
LIHC += u'3 z U U S ! _ 1 " s ! 0 a v V 1 ~ '
# Lyrics
Lyrics = u'Lord,_ I have cried_ un-to_ Thee,_ heark-en un-to me; '
Lyrics += u'hear-ken_ un-to_ me,_ O_ Lord.'

bnLIHC = neume_dict.translate(LIHC)
LIHCneumes = bnLIHC.split(" ")

# page layout
c = canvas.Canvas("C:\\Users\\John\\Documents\\PythonTests\\ByzWrite\\test.pdf",
                  pagesize = letter)
pageWidth, pageHeight = letter
leftMargin, rightMargin = 72,72
topMargin, bottomMargin = 72,72

# page size
pageSize = letter
# line height
lineHeight = 72
# header height
headerHeight = 0

Nc = Cursor(leftMargin,pageSize[1]-topMargin)
Nc.y -= lineHeight - headerHeight


c.setFont("EZPsaltica",24)
#t = c.beginText()
#t.setFont('EZPsaltica',24)
#t.setCharSpace(0.2)
#t.setTextOrigin(Nc.x,Nc.y)
#t.textLine(bnLIHC)

print("Dict len: " + str(len(LIHCneumes)))

for neume in LIHCneumes:
    print("Neume length: " + str(pdfmetrics.stringWidth(neume,'EZPsaltica',24)))
    neumeLength = pdfmetrics.stringWidth(neume,'EZPsaltica',24)
    if (Nc.x + neumeLength >= pageWidth - rightMargin): # runs over right margin
        Nc.x = leftMargin
        Nc.y -= lineHeight
        c.drawString(Nc.x,Nc.y,neume)
    else:
        c.drawString(Nc.x,Nc.y,neume)
    Nc.x += neumeLength
    
    #Nc.x += pdfmetrics.stringWidth(neume,'EZPsaltica',24)
    #if Nc.x > (pageWidth - rightMargin):
    #    Nc.x = leftMargin
    #    Nc.y -= lineHeight
    


#print("String length: " + str(pdfmetrics.stringWidth(bnLIHC,'EZPsaltica',24)))


c.showPage()
c.save()


