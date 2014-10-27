# -*- coding: utf8 -*-

'''
Create a 'song' consisting of three layers:

  A) an ambient atmospheric background layer
  [TODO] B) foreground material (like an instrument playing, or spoken word)
  [TODO] C) random sound effects (like telephones, horns, other short sounds)

The following directory structure is assumed:

    .
    ├── audio
    │   ├── backgrounds
    │   │   ├── city
    │   │   ├── nature
    │   │   └── uboat
    │   └── foregrounds
    │       ├── afloat
    │       ├── divers
    │       └── fbi
    └── src

The 'backgrounds' directory contains subdirectories with sample files in them which are all
part of a common theme. (I.e., the song generator doesn't use background sounds from both
city and nature).

'''
    

import os
import random
import glob
import jumpcity

CROSSFADE = 4 # Duration of crossfades, in seconds.
BGPARTS = 4 # Number of parts in the background.
MINDUR = 6 # Minimum duration of a background fragment.
MAXDUR = 15 # Maximum duration of a background fragment.

# For the background layer: choose a style, and take BGPARTS random segments from that.
backgroundstyles = []
for fn in glob.glob("../audio/backgrounds/*"):
    backgroundstyles.append(fn)
backgroundstyle = random.choice(backgroundstyles)
print "Creating a song with a '%s' background style" % backgroundstyle.split("/")[-1]

# What background files are there for this style?
backgroundfiles = []
for fn in glob.glob(os.path.join(backgroundstyle, "*")):
    backgroundfiles.append(fn)
    
class BackgroundTrack(object):
    def __init__(self, filename):
        self.filename = filename
        self.duration = jumpcity.soundfileduration(filename)
        self.length = int(random.uniform(MINDUR, MAXDUR)) # Choose a fragment
        self.start = int(random.uniform(0, self.duration - self.length - CROSSFADE * 2)) # Let it come from anywhere in the source file.
        
    def __str__(self):
        return "Track %s duration %s, extract from %s to %s, duration %s" % \
            (self.filename, jumpcity.seconds2hhmmss(self.duration),
            jumpcity.seconds2hhmmss(self.start), 
            jumpcity.seconds2hhmmss(self.start + self.length),
            jumpcity.seconds2hhmmss(self.length)
            )

mixercmd = "sox -m "
cumul = 0.0
for nr, fn in enumerate(random.sample(backgroundfiles, BGPARTS)):
    tr = BackgroundTrack(fn)
    print tr
    
    if nr in (0, 3): 
        # First or last part.
        fadelength = tr.length + CROSSFADE / 2
        trimlength = tr.length + CROSSFADE
    else:
        # A part somewhere in the middle.
        fadelength = tr.length + CROSSFADE
        trimlength = tr.length + CROSSFADE * 2

    trimstart = max(0, (cumul - CROSSFADE / 2))
    trim = "trim %d %d" % (trimstart, trimlength)
    fade = "fade t %d %d %d" % (CROSSFADE, fadelength, CROSSFADE)

    delaylength = max(0, (cumul - CROSSFADE / 2))
    delay = "delay %d %d" % (delaylength, delaylength)
    cumul += tr.length

    ofn = "layer%d.wav" % nr
    soxcmd = "sox %s %s %s %s %s" % (tr.filename, ofn, trim, fade, delay)
    os.system(soxcmd)
    mixercmd += ofn + " "

mixercmd += " bg.wav"
os.system(mixercmd)
os.system("play -q bg.wav")
