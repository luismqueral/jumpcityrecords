# -*- coding: utf-8 -*-

# HSL (Hue-Saturation-Lightness) to RGB conversion.
# Software by Michiel Overtoom, motoom@xs4all.nl, november 2010
# Algorithm taken from http://en.wikipedia.org/wiki/HSL_and_HSV

import unittest

# Given an HSL color with hue H ∈ [0°, 360°), saturation SHSL ∈ [0, 1], and lightness L ∈ [0, 1],
# compute R,G,B (each component in 0..1)
def hsl2rgb1(h, s, l):
    c = (1 - abs(2 * l - 1)) * s
    ha = float(h) / 60.0
    x = c * (1 - abs(ha % 2 - 1))
    r = g = b = 0
    if ha < 1:
        r, g, b = c, x, 0
    elif ha < 2:
        r, g, b = x, c, 0
    elif ha < 3:
        r, g, b = 0, c, x
    elif ha < 4:
        r, g, b = 0, x, c
    elif ha < 5:
        r, g, b = x, 0, c
    elif ha < 6:
        r, g, b = c, 0, x
    else:
        r, g, b = 0, 0, 0
    m = l - c / 2.0
    return r + m, g + m, b + m

# Same as hsl2rgb1, but returns r,g,b, values in 0..255 inclusive.
def hsl2rgb(h, s, l):
    r, g, b = hsl2rgb1(h, s, l)
    return int(round(255 * r)), int(round(255 * g)), int(round(255 * b))


class HslTests(unittest.TestCase):
    def test_conversion(self):
        "Tests taken from the page http://en.wikipedia.org/wiki/HSL_and_HSV, 'Examples' table"
        wikipediatable="""
            #FFFFFF 	1.000 	1.000 	1.000 	n/a 	n/a 	0.000 	0.000 	1.000 	1.000 	1.000 	1.000 	0.000 	0.000 	0.000
            #808080 	0.500 	0.500 	0.500 	n/a 	n/a 	0.000 	0.000 	0.500 	0.500 	0.500 	0.500 	0.000 	0.000 	0.000
            #000000 	0.000 	0.000 	0.000 	n/a 	n/a 	0.000 	0.000 	0.000 	0.000 	0.000 	0.000 	0.000 	0.000 	0.000
            #FF0000 	1.000 	0.000 	0.000 	0.0° 	0.0° 	1.000 	1.000 	1.000 	0.500 	0.333 	0.299 	1.000 	1.000 	1.000
            #BFBF00 	0.750 	0.750 	0.000 	60.0° 	60.0° 	0.750 	0.750 	0.750 	0.375 	0.500 	0.664 	1.000 	1.000 	1.000
            #008000 	0.000 	0.500 	0.000 	120.0° 	120.0° 	0.500 	0.500 	0.500 	0.250 	0.167 	0.293 	1.000 	1.000 	1.000
            #80FFFF 	0.500 	1.000 	1.000 	180.0° 	180.0° 	0.500 	0.500 	1.000 	0.750 	0.833 	0.850 	0.500 	1.000 	0.400
            #8080FF 	0.500 	0.500 	1.000 	240.0° 	240.0° 	0.500 	0.500 	1.000 	0.750 	0.667 	0.557 	0.500 	1.000 	0.250
            #BF40BF 	0.750 	0.250 	0.750 	300.0° 	300.0° 	0.500 	0.500 	0.750 	0.500 	0.583 	0.457 	0.667 	0.500 	0.571
            #A0A424 	0.628 	0.643 	0.142 	61.8° 	61.5° 	0.501 	0.494 	0.643 	0.393 	0.471 	0.581 	0.779 	0.638 	0.699
            #411BEA 	0.255 	0.104 	0.918 	251.1° 	250.0° 	0.814 	0.750 	0.918 	0.511 	0.426 	0.242 	0.887 	0.832 	0.756
            #1EAC41 	0.116 	0.675 	0.255 	134.9° 	133.8° 	0.559 	0.504 	0.675 	0.396 	0.349 	0.460 	0.828 	0.707 	0.667
            #F0C80E 	0.941 	0.785 	0.053 	49.5° 	50.5° 	0.888 	0.821 	0.941 	0.497 	0.593 	0.748 	0.944 	0.893 	0.911
            #B430E5 	0.704 	0.187 	0.897 	283.7° 	284.8° 	0.710 	0.636 	0.897 	0.542 	0.596 	0.423 	0.792 	0.775 	0.686
            #ED7651 	0.931 	0.463 	0.316 	14.3° 	13.2° 	0.615 	0.556 	0.931 	0.624 	0.570 	0.586 	0.661 	0.817 	0.446
            #FEF888 	0.998 	0.974 	0.532 	56.9° 	57.4° 	0.466 	0.454 	0.998 	0.765 	0.835 	0.931 	0.467 	0.991 	0.363
            #19CB97 	0.099 	0.795 	0.591 	162.4° 	163.4° 	0.696 	0.620 	0.795 	0.447 	0.495 	0.564 	0.875 	0.779 	0.800
            #362698 	0.211 	0.149 	0.597 	248.3° 	247.3° 	0.448 	0.420 	0.597 	0.373 	0.319 	0.219 	0.750 	0.601 	0.533
            #7E7EB8 	0.495 	0.493 	0.721 	240.5° 	240.4° 	0.228 	0.227 	0.721 	0.607 	0.570 	0.520 	0.316 	0.290 	0.135
            """.replace("°", "").replace("n/a","0.0")
        err = 0.001
        for line in [x.strip() for x in wikipediatable.splitlines()]:
            if not line: continue
            htmlcolor, refr, refg, refb, h, _, _, _, _, l, _, _, _, shsl, _ = line.split()
            refr, refg, refb, h, s, l = float(refr), float(refg), float(refb), float(h), float(shsl), float(l)
            r, g, b = hsl2rgb1(h, s, l)
            dr, dg, db = abs(refr - r), abs(refg - g), abs(refb - b)
            self.assertFalse(dr > err or dg > err or db > err)

    def test_eightbitquantities(self):
        self.assertEqual(hsl2rgb(0.0, 0.0, 0.0), (0, 0, 0))
        self.assertEqual(hsl2rgb(0.0, 0.0, 0.5), (128, 128, 128))
        self.assertEqual(hsl2rgb(0.0, 0.0, 1.0), (255, 255, 255))
        
if __name__ == "__main__":
    unittest.main()
            
