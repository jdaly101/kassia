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
        
class Glyph:
    def __init__(self,neumes='',neumePos=[],lyrics='',lyricsPos=[],fthora='',fthoraPos=[]):
        self.neumes = neumes
        self.neumePos = neumePos
        self.lyrics = lyrics
        self.lyricsPos = lyricsPos
        self.fthora = fthora
        self.fthoraPos = fthoraPos
         
        self.nWidth = 0     # neume width
        self.lWidth = 0     # lyric width
        self.width  = 0     # glyph width
         
    def calc_width(self,neumeFont="EZPsaltica",neumeFontSize=20,
                    lyricFont="EZOmega",lyricFontSize=12)
        self.nWidth = pdfmetrics.stringWidth(self.neumes,neumeFont,neumeFontSize)
        self.lWidth = pdfmetrics.stringWidth(self.lyrics,lyricFont,lyricFontSize)
        self.width = max(self.nWidth,self.lWidth)
        
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
        self.nFontSize = 20
        self.lFontSize = 12
        
        psalticaTTF = "fonts/EZ Psaltica.TTF"
        oxeiaTTF    = "fonts/EZ Oxeia.ttf"
        omegaTTF    = "fonts/EZ Omega.ttf"
        pdfmetrics.registerFont(TTFont("EZPsaltica",psalticaTTF,asciiReadable=True))
        pdfmetrics.registerFont(TTFont("EZOxeia",oxeiaTTF))
        pdfmetrics.registerFont(TTFont("EZOmega",omegaTTF))
        
        c = canvas.Canvas(self.outFile,pagesize = letter)
        
        
        # For each tropar
        for troparion in self.bnml.iter('troparion'):
            neumesText = " ".join(troparion.find('neumes').text.strip().split())
            lyricsText = " ".join(troparion.find('lyrics').text.strip().split())
            nPos,lPos = self.linebreak(neumesText,lyricsText)
            
            for glyph in nPos:
                c.setFont("EZPsaltica",self.nFontSize)
                c.drawString(glyph[0]+self.leftmargin,glyph[1] + 600,glyph[2])
                print glyph
            for lyric in lPos:
                c.setFont("EZOmega",self.lFontSize)
                c.drawString(lyric[0]+self.leftmargin,lyric[1] + 600,lyric[2])
                print lyric
            
        c.showPage()
        try:
            c.save()
        except IOError:
            print "Could not save file"
            
    def addable_neume(neume):
        # See if neume should be added
        # I think neumes that don't take lyrics should cover most cases
        return(not neume_dict.takes_lyric(neume))
            
    def makeGlyphArray(self,neumes,lyrics = None):
        neumeArray = neumes.split( )
        lyricArray = re.split(' ',lyrics)
        
        i = 0
        while(i < len(neumeArray)):
            # Grab next neume
            n = neumeArray[i]
            
            # Add more neumes to glyph? Like fthora, ison, etc
            j = 1
            while(addable_neume(neumeArray[i+j])):
                j += 1
            i += j
        # Does neume call for lyric?
            # Add in lyric
            # If lyric ends with _
                # See how many neumes to put in glyph
        # Create glyph
        # Calculate width
        # Add glyph to list
            
            
    def linebreak(self,neumes,lyrics = None):
        """Break neumes and lyrics into lines"""
        cr = Cursor(0,0)
        lyricArray = re.split(' ',lyrics)
        # If lyric spans multiple neumes
        #   then see if lyric is wider than span
        #   else see if width of glypch is max of neume and lyric
        charSpace = 4 # default space between characters
        textOffset = 30 # default space lyrics appear below neumes
        #neumeArray = neume_dict.translate(neumes).split(' ')
        neumeArray = neumes.split(' ')
        neumePos = []
        lyricPos = []
        lyricIdx = 0
        for neume in neumeArray:
            #print("Neume length: " + str(pdfmetrics.stringWidth(neume,'EZPsaltica',24)))
            nWidth = pdfmetrics.stringWidth(neume_dict.translate(neume),'EZPsaltica',self.nFontSize)
            if nWidth > 1.0: # if it's not a gorgon or other small symbol
                # Neume might take lyric
                if lyricIdx < len(lyricArray):
                    lyr = lyricArray[lyricIdx]
                else:
                    lyr = ""
                lWidth = pdfmetrics.stringWidth(lyr,'EZOmega',self.lFontSize)
                # Glyph width will be the max of the two if lyric isn't stretched out
                # across multiple neumes
                addLyric = False
                #if (lyr[-1] != "_") & (neume_dict.takesLyric(neume)):
                if (neume_dict.takesLyric(neume)):
                    glWidth = max(nWidth,lWidth)
                    lyricIdx += 1
                    addLyric = True
                else:
                    glWidth = nWidth
                if (glWidth + cr.x) >= self.lineWidth: # line break
                    cr.x, cr.y = 0, cr.y - self.lineHeight
                    # does it take a lyric syllable?
                    neumePos.append((cr.x,cr.y,neume_dict.translate(neume)))
                else: # no line break
                    # does it take a lyric syllable?
                    neumePos.append((cr.x,cr.y,neume_dict.translate(neume)))
                if (addLyric):
                    lyricPos.append((cr.x,cr.y-textOffset,lyr))
                cr.x += glWidth + charSpace
                
            else:
                # offsets for gorgon
                # offsets for apli
                # offset for kentima
                # offsets for omalon
                # offsets for antikenoma
                # offsets for eteron
                neumePos.append((cr.x - charSpace,cr.y,neume_dict.translate(neume)))
            
        #print neumePos
        return neumePos, lyricPos
        

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
            