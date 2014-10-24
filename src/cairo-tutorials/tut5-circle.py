#!/usr/bin/python

'''
ZetCode PyCairo tutorial 

This code example draws a circle
using the PyCairo library.

author: Jan Bodnar
website: zetcode.com 
last edited: August 2012

http://zetcode.com/gfx/pycairo/basicdrawing/
'''


from gi.repository import Gtk
import cairo
import math
import random

class Example(Gtk.Window):

    def __init__(self):
        super(Example, self).__init__()
        
        self.init_ui()
        
        
    def init_ui(self):    

        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)

        self.set_title("Fill & stroke")
        self.resize(230, 150)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        
    
    def on_draw(self, wid, cr):

        cr.set_line_width(9)
        cr.set_source_rgb(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
        
        w, h = self.get_size()      

        cr.translate(w/3, h/3)
        cr.arc(0, 0, h/4, 0, 2*math.pi)
        cr.stroke_preserve()
        
        cr.set_source_rgb(random.uniform(0,1), random.uniform(0,1), random.uniform(0,1))
        cr.fill()
        
    
def main():
    
    app = Example()
    Gtk.main()
        
        
if __name__ == "__main__":    
    main()
