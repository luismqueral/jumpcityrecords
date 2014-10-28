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

assets = []
for fn in glob.glob("../audio/_assets/*"):
    assets.append(fn)
asset = random.choice(assets)
print "Creating a track from '%s' asset" % asset

fns = []
for fn in glob.glob(os.path.join(asset, "*")):
    fns.append(fn)
    
mixercmd = "sox -m "
for fn in random.sample(fns, 3):
    print "   ", fn
    mixercmd += '"%s" ' % fn

trackname = "track-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
mixercmd += trackname
print "Mixing to %s..." % trackname, 
os.system(mixercmd)
print "done"

os.system("play -q %s" % trackname)
