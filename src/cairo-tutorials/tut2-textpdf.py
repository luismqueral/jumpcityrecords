#!/usr/bin/python

'''
ZetCode PyCairo tutorial 

This program uses PyCairo to 
produce a PDF image.

author: Jan Bodnar
website: zetcode.com 
last edited: August 2012
'''

import cairo
       
    
def main():
    
    ps = cairo.PDFSurface("tut2.pdf", 504, 648)
    cr = cairo.Context(ps)
    
    cr.set_source_rgb(0, 0, 0)
    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(40)
    
    cr.move_to(10, 50)
    cr.show_text("Disziplin ist Macht.")
    cr.show_page()
        
        
if __name__ == "__main__":    
    main()
