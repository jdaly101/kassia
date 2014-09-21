import neume_dict

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

import sys
import xml.etree.ElementTree as ET
import re

class Cursor:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
class Kassia:
    """Base class for package"""
    def __init__(self,fileName,outFile = "out.pdf"):
        print "Making a Kassia..."
        self.fileName = fileName # input file
        self.outFile = outFile # output file
        try:
            open(fileName,"r")
            fileReadable = True
        except IOError:
            fileReadable = False
            print "Not readable"
        
        if fileReadable:
            self.parseFile()
            self.createPDF()
        
    def parseFile(self):
        print "Will it parse?"
        try:
            bnmlTree = ET.parse(self.fileName)
            bnml = bnmlTree.getroot()
            self.bnml = bnml   
               
        except ET.ParseError:
            print "Failed to parse XML file"
            
    def createPDF(self):
        """Create PDF output file"""
        # TODO: Parse page layout and formatting
        self.paperSize = letter
        self.topmargin = 72
        self.bottommargin = 72
        self.leftmargin = 72
        self.rightmargin = 72
        self.lineHeight = 72
        self.lineWidth = self.paperSize[0] - (self.leftmargin + self.rightmargin)
        
        psalticaTTF = "fonts/EZ Psaltica.TTF"
        oxeiaTTF    = "fonts/EZ Oxeia.ttf"
        pdfmetrics.registerFont(TTFont("EZPsaltica",psalticaTTF,asciiReadable=True))
        pdfmetrics.registerFont(TTFont("EZOxeia",oxeiaTTF))
        
        c = canvas.Canvas(self.outFile,pagesize = letter)
        
        
        # For each tropar
        for troparion in self.bnml.iter('troparion'):
            neumesText = " ".join(troparion.find('neumes').text.strip().split())
            lyricsText = " ".join(troparion.find('lyrics').text.strip().split())
            nPos = self.linebreak(neumesText,lyricsText)
            
            for glyph in nPos:
                c.setFont("EZPsaltica",20)
                c.drawString(glyph[0]+self.leftmargin,glyph[1] + 600,glyph[2])
                print glyph
                
        c.showPage()
        try:
            c.save()
        except IOError:
            print "Could not save file"
            
            
    def linebreak(self,neumes,lyrics = None):
        """Break neumes and lyrics into lines"""
        cr = Cursor(0,0)
        lyricArray = re.split(' ',lyrics)
        # If lyric spans multiple neumes
        #   then see if lyric is wider than span
        #   else see if width of glypch is max of neume and lyric
        charSpace = 4 # default space between characters
        textOffset = 30 # default space lyrics appear below neumes
        neumeArray = neume_dict.translate(neumes).split(' ')
        neumePos = []
        lyrIdx = 0
        for neume in neumeArray:
            #print("Neume length: " + str(pdfmetrics.stringWidth(neume,'EZPsaltica',24)))
            nWidth = pdfmetrics.stringWidth(neume,'EZPsaltica',20)
            if nWidth > 1.0: # if it's not a gorgon or other small symbol
                if (nWidth + cr.x) >= self.lineWidth: # line break
                    cr.x, cr.y = 0, cr.y - self.lineHeight
                    # does it take a lyric syllable?
                    neumePos.append((cr.x,cr.y,neume))
                else: # no line break
                    # does it take a lyric syllable?
                    neumePos.append((cr.x,cr.y,neume))
                cr.x += nWidth + charSpace
            else:
                # offsets for gorgon
                # offsets for apli
                # offset for kentima
                # offsets for omalon
                # offsets for antikenoma
                # offsets for eteron
                neumePos.append((cr.x - charSpace,cr.y,neume))
            
        #print neumePos
        return neumePos
        

def main(argv):
    if len(argv) == 1:
        kas = Kassia(argv[0])
    elif len(argv) > 1:
        kas = Kassia(argv[0],argv[1])
    
if __name__ == "__main__":
    print "Starting up..."
    if len(sys.argv) == 1:
        print "Input XML file required"
        sys.exit(1)
    main(sys.argv[1:])
            