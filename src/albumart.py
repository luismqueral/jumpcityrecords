
"""
albumart.py

Using Cairo or PIL to draw album art. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import os
import datetime
try:
    import cairo # On Ubuntu: sudo apt-get install python-cairo; On OSX (with homebrew): sudo brew install py2cairo
    have_cairo = True
except ImportError:
    from PIL import Image, ImageFont, ImageDraw # On OSX: sudo pip install pillow
    have_cairo = False
import colorspace
import utils
from utils import rnd
import rotate
from rotate import Rectangle, Point
import constants

def randomcolor(transfrom=None, transto=None):
    if transfrom is None:
        return rnd(1), rnd(1), rnd(1)
    else:
        return rnd(1), rnd(1), rnd(1), rnd(transfrom, transto)


def randompastelcolor():
    hue = rnd(360)
    lightness = rnd(0.8, 0.9)
    saturation = rnd(0.5, 1)
    return colorspace.hsl2rgb1(hue, saturation, lightness)
    

def randomrectangle_candidate(w, h):
    center = Point(rnd(w), rnd(h))
    rw = max(rnd(w * 0.9), 30) # Not too thin: minimum width and height 20 pixels.
    rh = max(rnd(h * 0.9), 20)
    r = Rectangle(
        Point(center.x - rw / 2, center.y + rh / 2),
        Point(center.x + rw / 2, center.y + rh / 2),
        Point(center.x + rw / 2, center.y - rh / 2),
        Point(center.x - rw / 2, center.y - rh / 2))
    # Now rotate it randomly. There's a fifty-fifty percent change that the rotation will be strongly vertical/horizontal aligned.
    if rnd(100) > 50:
        angle = rnd(360) # Completely arbitrary rotation.
    else:
        angle = rnd(4) - 2 # Almost horizontal/vertical ;-)
    r = rotate.rotatedrectangle(r, angle)
    # Check whether every coordinate of the rectangle lies within (0,0)-(w,h) (with a 5% margin)
    topmargin, rightmargin, bottommargin, leftmargin = h * 0.05, w * 0.95, h * 0.95, w * 0.05 
    for p in r:
        if p.x < leftmargin or p.x > rightmargin: return None
        if p.y < topmargin or p.y > bottommargin: return None
    return r


def randomrectangle(w, h):
    r = None
    while not r:
        r = randomrectangle_candidate(w, h)
    return r


def drawrectangle(cr, r):
    for p in r:
        cr.line_to(p.x, p.y)
    cr.fill()
    

def render(cr, w, h, albumtitle=None, datestamp=None):
    if datestamp is None:
        datestamp = datetime.datetime.now().strftime("%Y-%m-%d / %H:%M:%S")
    if have_cairo:
        splith = h * 0.85
        # Start with white background.
        cr.set_source_rgb(1, 1, 1) # White.
        cr.rectangle(0, 0, w, h)
        cr.fill()
        # Colored upper pane (backdrop for rectangles).
        cr.set_source_rgba(*randomcolor(0.8, 0.9))
        cr.rectangle(0, 0, w, splith)
        cr.fill()
        # Figure.
        cr.set_line_width(0)
        if w > 100 and h > 100: # Refuse to draw in too small a space.
            for i in xrange(2): # Draw two rectangles.
                cr.set_source_rgb(*randompastelcolor())
                r = randomrectangle(w, splith)
                drawrectangle(cr, r)
                cr.fill()
        # Date and time
        cr.set_source_rgb(0.5, 0.5, 0.5) # Gray.
        cr.select_font_face("Orator", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(h * 0.065)
        baseline = h * 0.95
        _, _, textw, _, _, _ = cr.text_extents(datestamp)
        cr.move_to(w / 2 - textw / 1.95, baseline) # Center text horizontally.
        cr.show_text(datestamp)
        # Outline.
        cr.rectangle(0, 0, w, h)
        cr.set_source_rgb(0.85, 0.85, 0.85) # Light gray.
        cr.set_line_width(1)
        cr.stroke()
    else:
        # TODO: Finish this code path.
        splith = h * 0.87
        # Colored, transparent upper pane.
        draw = ImageDraw.Draw(cr, "RGBA")
        color = tuple([int(val * 255) for val in randomcolor(0.8, 0.9)])
        draw.rectangle((0, 0, w, splith), color)
        #
        draw = ImageDraw.Draw(cr, "RGB")
        # Figure.
        if w > 100 and h > 100:
            for i in xrange(2):
                color = tuple([int(val * 255) for val in randompastelcolor()])
                r = randomrectangle(w, splith)
                draw.polygon(r, color)
        # Date and time.
        color = (128, 128, 128)
        fnt = ImageFont.truetype("fonts/Orator-regular.ttf", int(w * 0.07))
        baseline = h * 0.89       
        textw, texth = fnt.getsize(datestamp)
        draw.text((w / 2 - textw / 2, baseline), datestamp, font=fnt, fill=color)
        # Outline.
        color = (216, 216, 216)
        draw.rectangle((0, 0, w - 1, h - 1), fill=None, outline=color)


def rendertopng(albumtitle, datestamp, albumdir):
    w = h = constants.ALBUMARTSIZE
    filename = os.path.join(albumdir, albumtitle + ".png")
    if have_cairo:
        ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        cr = cairo.Context(ims)
        render(cr, w, h, albumtitle, datestamp)
        ims.write_to_png(filename)
    else:
        cr = Image.new("RGB", (w * 2, h * 2), "#fff")
        render(cr, w * 2, h * 2, albumtitle, datestamp)
        cr.thumbnail((w, h), Image.ANTIALIAS)
        cr.save(filename)
    return filename
    
            
if __name__ == "__main__":
    # Generate some example images, store them in the 'output' subdirectory.
    if not os.path.exists("output"):
        os.mkdir("output")
    if 1:
        print "Generating album art pictures in ./output directory:"
        for i in xrange(1):
            w, h = 725, 725
            albumtitle = utils.randomname()
            filename = os.path.join("output", albumtitle + ".png")
            if have_cairo:
                ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
                cr = cairo.Context(ims)
                render(cr, w, h, albumtitle)     
                ims.write_to_png(filename)
            else:
                cr = Image.new("RGB", (w * 2, h * 2), "#fff")
                render(cr, w * 2, h * 2, albumtitle)
                cr.thumbnail((w, h), Image.ANTIALIAS)
                cr.save(filename)
