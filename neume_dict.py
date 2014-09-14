#!/usr/bin/python
import re

def translate(text):
    #myDict = dict((re.escape(k), v) for k, v in ezPsaltica.iteritems())
    #pattern = re.compile("|".join(myDict.keys()))
    #reptext = pattern.sub(lambda m: myDict[re.escape(m.group(0))], text)
    #return reptext
    splitText = text.split(" ")
    tmpText = [ezPsaltica[t] if ezPsaltica.has_key(t) else t for t in splitText]
    #print tmpText
    #print tmpText.__class__
    #print " ".join(tmpText)
    #return u'\uF020\uF020'.join(tmpText)
    return u' '.join(tmpText)
    
    ezPsaltica1 = {
    ' ' : u'\uF020',
    'i' : u'\uF030',
    'ip' : u'\uF070',
    'o' : u'\uF031',
    'o2' : u'\uF032',
    'o3' : u'\uF033',
    'o4' : u'\uF034',
    'o5' : u'\uF035',
    'o6' : u'\uF036',
    'o7' : u'\uF037',
    'o8' : u'\uF038',
    'o9' : u'\uF039',
    '`' : u'\uF060',
    '~' : u'\uF07E',
    '=' : u'\uF03D',
    'p' : u'\uF071',
    'p2' : u'\uF077',
    'p3' : u'\uF065',
    'p4' : u'\uF072',
    'p5' : u'\uF074',
    'p6' : u'\uF079',
    'p7' : u'\uF075',
    'p8' : u'\uF069',
    'a' : u'\uF021',
    'a2' : u'\uF040',
    'se' : u'\uF05F',
    'e' : u'\uF029',
    #'-' : u'\uF02D', #
    'a3' : u'\uF023',
    'a4' : u'\uF024',
    'a5' : u'\uF025',
    'a6' : u'\uF05E',
    'a7' : u'\uF026',
    'a8' : u'\uF02A',
    'a9' : u'\uF028',
    'ap' : u'\uF051',
    'ap2' : u'\uF057',
    'ap3' : u'\uF045',
    'oi' : u'\uF04E',
    'io' : u'\uF0CE',
    #'l' : u'\uF06C', #
    #'L' : u'\uF04C', #
    'ik' : u'\uF050',
    'as' : u'\uF049',
    '1k' : u'\uF055',
    '2k' : u'\uF059',
    '3k' : u'\uF054',
    '4k' : u'\uF052',
    'g' : u'\uF053',
    #'S' : u'\uF073',#
    'gb' : u'\uF078',
    #'X' : u'\uF058',#
    #'dg' : u'\uF068',#
    #'H' : u'\uF048',#
    'D' : u'\uF064',
    #'D' : u'\uF044',#
    'T' : u'\uF066',
    #'F' : u'\uF046',#
    'r' : u'\uF067', # argon
    'R' : u'\uF047',
    'l' : u'\uF03B',
    #':' : u'\uF03A',#
    'l2' : u'\uF06B',
    #'K' : u'\uF04B',#
    'k' : u'\uF061',
    #'A' : u'\uF041',#
    'kb' : u'\uF091',
    #'Z' : u'\uF07A', # or maybe \uf091
    'v' : u'\uF05C',
    'pf' : u'\uF027',
    's' : u'\uF022',
    #'}' : u'\uF07D',#
    'ot' : u'\uF07B', # this and next could be switched
    'om' : u'\uF05B',
    'E' : u'\uF05D',
    'b' : u'\uF04A',
    'br' : u'\uF06A',
 #   '' : u'', # place holder for CtrlAlt-C character
    'ni' : u'\uF063',
    'pa' : u'\uF076',
    'vou' : u'\uF062',
    'ga' : u'\uF06E',
    'dhi' : u'\uF06D',
    'ke' : u'\uF02C',
    'zo' : u'\uF02E',
    'hn' : u'\uF02F',
    '+' : u'\uF02B',
#    '' : u'', # Place holder for Alt 0186
    'vr' : u'\uF07C',
    'C' : u'\uF043',
    'V' : u'\uF056',
    'B' : u'\uF042',
    'N' : u'\uF04E',
    'M' : u'\uF04D',
    '>' : u'\uF03E',
    '?' : u'\uF03F',
    '<' : u'\uF03C'}
    

ezPsaltica = {
    #' ' : u'\uF020',
    '0' : u'\uF030',
    'p' : u'\uF070',
    '1' : u'\uF031',
    '2' : u'\uF032',
    '3' : u'\uF033',
    '4' : u'\uF034',
    '5' : u'\uF035',
    '6' : u'\uF036',
    '7' : u'\uF037',
    '8' : u'\uF038',
    '9' : u'\uF039',
    '`' : u'\uF060',
    '~' : u'\uF07E',
    '=' : u'\uF03D',
    'q' : u'\uF071',
    'w' : u'\uF077',
    'e' : u'\uF065',
    'r' : u'\uF072',
    't' : u'\uF074',
    'y' : u'\uF079',
    'u' : u'\uF075',
    'i' : u'\uF069',
    '!' : u'\uF021',
    '@' : u'\uF040',
    '_' : u'\uF05F',
    ')' : u'\uF029',
    '-' : u'\uF02D',
    '#' : u'\uF023',
    '$' : u'\uF024',
    '%' : u'\uF025',
    '^' : u'\uF05E',
    '&' : u'\uF026',
    '*' : u'\uF02A',
    '(' : u'\uF028',
    'Q' : u'\uF051',
    'W' : u'\uF057',
    'E' : u'\uF045',
    'O' : u'\uF04F',
    'o' : u'\uF0CE',
    'l' : u'\uF06C',
    'L' : u'\uF04C',
    'P' : u'\uF050',
    'I' : u'\uF049',
    'U' : u'\uF055',
    'Y' : u'\uF059',
    'T' : u'\uF054',
    'R' : u'\uF052',
    'S' : u'\uF053',
    's' : u'\uF073',
    'x' : u'\uF078',
    'X' : u'\uF058',
    'h' : u'\uF068',
    'H' : u'\uF048',
    'd' : u'\uF064',
    'D' : u'\uF044',
    'f' : u'\uF066',
    'F' : u'\uF046',
    'g' : u'\uF067',
    'G' : u'\uF047',
    ';' : u'\uF03B',
    ':' : u'\uF03A',
    'k' : u'\uF06B',
    'K' : u'\uF04B',
    'a' : u'\uF061',
    'A' : u'\uF041',
    'z' : u'\uF091',
    'Z' : u'\uF07A', # or maybe \uf091
    '\\' : u'\uF05C',
    '\'' : u'\uF027',
    '"' : u'\uF022',
    '}' : u'\uF07D',
    '[' : u'\uF07B', # this and next could be switched
    '{' : u'\uF05B',
    ']' : u'\uF05D',
    'J' : u'\uF04A',
    'j' : u'\uF06A',
 #   '' : u'', # place holder for CtrlAlt-C character
    'c' : u'\uF063',
    'v' : u'\uF076',
    'b' : u'\uF062',
    'n' : u'\uF06E',
    'm' : u'\uF06D',
    ',' : u'\uF02C',
    '.' : u'\uF02E',
    '/' : u'\uF02F',
    '+' : u'\uF02B',
#    '' : u'', # Place holder for Alt 0186
    '|' : u'\uF07C',
    'C' : u'\uF043',
    'V' : u'\uF056',
    'B' : u'\uF042',
    'N' : u'\uF04E',
    'M' : u'\uF04D',
    '>' : u'\uF03E',
    '?' : u'\uF03F',
    '<' : u'\uF03C'}