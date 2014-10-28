# -*- coding: utf8 -*-

import os
import random
import glob
import datetime

""" Create a track from random assets
- Choose a random directory from the _assets subdirectory.
- Choose three random files in this subdirectory.
- Mix them.
"""

asset = random.choice(glob.glob("../audio/_assets/*"))
print "Creating a track from '%s' asset" % asset
fns = glob.glob(os.path.join(asset, "*"))    

mixercmd = "sox -m "
for nr, fn in enumerate(random.sample(fns, 3)):
    print "   ", fn
    panning = (
        "1 2", # No panning for sample #1
        "1 2v0.25", # Right panning for sample #2
        "1v0.25 2", # Left panning for sample #3
        )
    layerfn = "layer%d.wav" % nr
    cmd = 'sox "%s" "%s" remix %s' % (fn, layerfn, panning[nr])
    print cmd
    os.system(cmd)
    
    mixercmd += '"%s" ' % layerfn

trackname = "track-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
mixercmd += trackname
print "Mixing to %s..." % trackname, 
os.system(mixercmd)
print "done"

os.system("play -q %s" % trackname)
