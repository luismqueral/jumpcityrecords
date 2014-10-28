# -*- coding: utf8 -*-

import os
import random
import glob
import jumpcity
import datetime

""" Create a track from random assets
- Choose a random directory from the _assets subdirectory.
- Choose three random files in this subdirectory.
- Mix them.
"""

MAXDUR = 60 # Maximum duration of mix.

asset = random.choice(glob.glob("../audio/_assets/*"))
print "Creating a track from '%s' asset" % asset
fns = glob.glob(os.path.join(asset, "*"))    

mixercmd = "sox -m "
for nr, fn in enumerate(random.sample(fns, 3)):
    print "   ", fn
    # See how long the sample is, if it's longer than MAXDUR seconds, fade it out
    fade = ""
    if jumpcity.soundfileduration(fn) > MAXDUR:
        fade = "fade 0 %d 4" % MAXDUR
    panning = (
        "remix 1 2", # No panning for sample #1
        "remix 1 2v0.25", # Right panning for sample #2
        "remix 1v0.25 2", # Left panning for sample #3
        )
    layerfn = "layer%d.wav" % nr
    cmd = 'sox "%s" "%s" %s %s' % (fn, layerfn, panning[nr], fade)
    print cmd
    os.system(cmd)
    
    mixercmd += '"%s" ' % layerfn

trackname = "track-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
mixercmd += trackname
print "Mixing to %s..." % trackname, 
os.system(mixercmd)
print "done"

os.system("play -q %s" % trackname)
