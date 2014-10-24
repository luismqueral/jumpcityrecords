
"""
randomdraw.py

A simple GTK app to exercise the Album Art drawing. Software by Michiel Overtoom, motoom@xs4all.nl

Resize the app to draw a fresh Album cover art.
"""

from gi.repository import Gtk
import albumart

class Randomdrawer(Gtk.Window):

    def __init__(self):
        super(Randomdrawer, self).__init__()        
        self.init_ui()


    def init_ui(self):    
        darea = Gtk.DrawingArea()
        darea.connect("draw", self.on_draw)
        self.add(darea)
        self.resize(725, 725)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()
        

    def on_draw(self, wid, cr):
        w, h = self.get_size()
        self.set_title("Random Album Art (%dx%d) - Resize this window to redraw" % (w, h))
        albumart.render(cr, w, h)


if __name__ == "__main__":    
    app = Randomdrawer()
    Gtk.main()
