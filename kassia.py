import neume_dict

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

import sys
import xml.etree.ElementTree as ET

class Cursor:
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
class Kassia:
    """Base class for package"""
    def __init__(self,fileName):
        print "Making a Kassia..."
        self.fileName = fileName # input file
        #self.outFile = outFile # output file
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
            # for each hymn
            #for troparion in bnml:
            #    neumesText = " ".join(troparion.find('neumes').text.strip().split())
            #    lyricsText = " ".join(troparion.find('lyrics').text.strip().split())
                
                
        except ET.ParseError:
            print "Failed to parse XML file"
            
    def createPDF(self):
        """Create PDF output file"""
        # TODO: Page layout and formatting
        
        # For each tropar
        for troparion in self.bnml.iter('troparion'):
            neumesText = " ".join(troparion.find('neumes').text.strip().split())
            lyricsText = " ".join(troparion.find('lyrics').text.strip().split())
        

def main(argv):
    print "In main..."
    kas = Kassia(argv[0])
    
if __name__ == "__main__":
    print "Starting up..."
    main(sys.argv[1:])
            