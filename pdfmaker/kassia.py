import neume_dict
from glyphs import Glyph, GlyphLine

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
import reportlab.lib.colors as colors

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
        vSpace = self.paperSize[1] - self.topmargin  
        vert_pos = self.paperSize[1] - self.topmargin             
        
        # For each tropar
        for troparion in self.bnml.iter('troparion'):
            # Draw title if there is one
            title_elem = troparion.find('title')
            if (title_elem is not None):
                title_text = title_elem.text.strip()
                title_attrib = title_elem.attrib
                title_attrib = self.fill_title_dict(title_attrib)

                c.setFillColor(title_attrib['color'])
                
                vert_pos -= title_attrib['font_size'] + 10
                c.setFont('EZOmega',title_attrib['font_size'])
                c.drawCentredString(self.paperSize[0]/2,vert_pos,title_text)
                vert_pos -= 36
            c.setFillColor(colors.black)

            neumesText = " ".join(troparion.find('neumes').text.strip().split())
            lyricsText = " ".join(troparion.find('lyrics').text.strip().split())

            self.neumeFont = "EZPsaltica"
            self.neumeFontSize = 20
            self.lyricFont = "EZOmega"
            self.lyricFontSize = 12

            firstLineOffset = 0     # Offset from dropcap char
            lineSpacing = 72

            neumeChunks = neume_dict.chunkNeumes(neumesText)
            gArray = self.makeGlyphArray(neumeChunks,lyricsText)
            gArray = self.line_break2(gArray,firstLineOffset)
            
            for ga in gArray:
                # TO DO: check if cursor has reached the end of the page
                c.setFont(self.neumeFont,self.nFontSize)
                xpos = self.leftmargin + ga.neumePos
                ypos = vert_pos - (ga.lineNum + 1)*lineSpacing
                c.drawString(xpos,ypos, ga.neumes)

                lyricOffset = 10

                if (ga.lyrics):
                    ypos -= lyricOffset
                    xpos = self.leftmargin + ga.lyricPos
                    c.setFont(self.lyricFont,self.lFontSize)
                    #if (ga.lyrics[-1] == "_"):
                    #    ga.lyrics += "_"
                    c.drawString(xpos,ypos,ga.lyrics)



            
        c.showPage()
        try:
            c.save()
        except IOError:
            print "Could not save file"
            
            
    def makeGlyphArray(self,neumeChunks,lyrics = None):
        lyricArray = re.split(' ',lyrics)
        i, lPtr = 0, 0
        gArray = []
        while(i < len(neumeChunks)):
            # Grab next chunk
            nc = neumeChunks[i]
            if (neume_dict.takesLyric(nc[0])):
                # chunk needs a lyric
                if (lPtr < len(lyricArray)):
                    lyr = lyricArray[lPtr]
                else:
                    lyr = ' '
                lPtr += 1
                g = Glyph(neumes=neume_dict.translate(nc),lyrics=lyr)
                # To Do: see if lyric ends with '_' and if lyrics are
                # wider than the neume, then combine with next chunk
            else: 
                # no lyric needed
                g = Glyph(neume_dict.translate(nc))
            g.calc_width()
            
            gArray.append(g)
            i += 1
        return gArray

        
    def line_break2(self,glyphArray,firstLineOffset):
        """Break neumes and lyrics into lines, currently greedy
        Rework this to return a list of lines!!!!"""
        cr = Cursor(firstLineOffset,0)

        # should be able to override these params in xml
        charSpace = 2 # avg spacing between characters
        lineWidth = self.lineWidth

        nlines = 0
        for g in glyphArray:
            if (cr.x + g.width) >= lineWidth:
                cr.x = 0
                nlines += 1
            g.lineNum = nlines
            adjLyricPos, adjNeumePos = 0, 0
            if g.nWidth >= g.lWidth:
                # center text
                adjLyricPos = (g.width - g.lWidth) / 2.
                
            else:
                # center neume
                adjNeumePos = (g.width - g.nWidth) / 2.

            g.neumePos = cr.x + adjNeumePos
            g.lyricPos = cr.x + adjLyricPos
            cr.x += g.width + charSpace

        return glyphArray

            
    def linebreak(self,neumes,lyrics = None):
        """Break neumes and lyrics into lines"""
        cr = Cursor(0,0)
        lyricArray = re.split(' ',lyrics)
        # If lyric spans multiple neumes
        #   then see if lyric is wider than span
        #   else see if width of glypch is max of neume and lyric
        charSpace = 4 # default space between characters
        textOffset = 20 # default space lyrics appear below neumes
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

    def fill_title_dict(self, title_dict):
        if not title_dict.has_key('color'):
           tmp_col = colors.Color(0,0,1,1)
        else:
            """parse the color"""
            if title_dict['color'] == "blue":
                title_dict['color'] = colors.blue
            elif re.match("#[0-9a-fA-F]{6}",title_dict['color']):
                col = [z/255. for z in hex_to_rgb(title_dict['color'])]
                title_dict['color'] = colors.Color(col[0],col[1],col[2],1)
            else:
                title_dict['color'] = color.black
        
        if not title_dict.has_key('font_size'):
            title_dict['font_size'] = 14
        else:
            title_dict['font_size'] = int(title_dict['font_size'])
        
        if not title_dict.has_key('font'):
            title_dict['font'] = "EZOmega"

        return title_dict

def hex_to_rgb(x):
    x = x.lstrip('#')
    lv = len(x)
    return tuple(int(x[i:i+lv // 3], 16) for i in range(0,lv,lv // 3))

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
            