# -*- coding: utf8 -*-

'''
Create a 'song' consisting of three layers:

  A) an ambient atmospheric background layer
  B) foreground material (like an instrument playing, or spoken word)
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
import datetime

CROSSFADE = 4 # Duration of crossfades, in seconds.
BGPARTS = 4 # Number of parts in the background.
BGMINDUR = 10 # Minimum duration of a background fragment.
BGMAXDUR = 30 # Maximum duration of a background fragment.

FGPARTS = 4 # Nr. of foreground excerpts in the foreground track.

class Track(object):
    def __init__(self, filename, mindur, maxdur, fadedur=CROSSFADE):
        self.filename = filename
        self.duration = jumpcity.soundfileduration(filename)
        if not self.duration:
            raise ValueError("Soxi can't determine the duration of '%s'" % filename)
        self.length = int(random.uniform(mindur, maxdur)) # Choose a fragment
        self.start = int(random.uniform(0, self.duration - self.length - fadedur * 2)) # Let it come from anywhere in the source file.
        
    def __str__(self):
        return "Track %s duration %s, extract from %s to %s, duration %s" % \
            (self.filename, jumpcity.seconds2hhmmss(self.duration),
            jumpcity.seconds2hhmmss(self.start), 
            jumpcity.seconds2hhmmss(self.start + self.length),
            jumpcity.seconds2hhmmss(self.length)
            )

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
    
bgmixercmd = "sox -m "
cumul = 0.0
for nr, fn in enumerate(random.sample(backgroundfiles, BGPARTS)):
    tr = Track(fn, BGMINDUR, BGMAXDUR)
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
    bgmixercmd += ofn + " "

bgmixercmd += " bg.wav norm -6 vol 0.8"
os.system(bgmixercmd)

# Foreground. 
#
# First, make a list of all available foreground samples.
foregroundfns = []
for dir, subdirs, fns in os.walk("../audio/foregrounds"):
    for fn in fns:
        if fn.endswith(".wav"):
            foregroundfns.append(os.path.join(dir, fn))

# This records how many foreground tracks are simulateously playing on each second:
occupied = [0] * int(cumul)

while True:
    print "Building foreground candidate..."
    tracks = []
    trackfns = random.sample(foregroundfns, FGPARTS)
    for fn in trackfns: 
        print fn
        tr = Track(fn, 10, cumul - 10)
        tr.songstart = random.uniform(6, cumul - tr.length - 6)
        for sec in xrange(int(tr.songstart), int(tr.length)):
            occupied[sec] += 1
        tracks.append(tr)
        
    # We don't want too much silence in the foreground. If there is, try another candidate foreground track.
    silence = len([x for x in occupied if x == 0])
    silenceperc = float(silence) / cumul * 100.0
    if silenceperc > 30:
        print "Too much silence, retrying..."
        continue

    # Mix together the foreground components.
    fgmixercmd = "sox -m "
    for nr, tr in enumerate(tracks):
        FGFADE = 0.5
        fadelength = float(tr.length) + FGFADE # Short fades.
        trimlength = float(tr.length) + FGFADE * 2
        trimstart = max(0, (float(tr.start) - FGFADE / 2))
        trim = "trim %f %f" % (trimstart, trimlength)
        fade = "fade t %f %f %f" % (FGFADE, fadelength, FGFADE)

        delaylength = max(0, (float(tr.songstart) - FGFADE / 2))
        delay = "delay %f %f" % (delaylength, delaylength)

        # Random filters to apply.
        filters = (
            "highpass -2 8000 norm -6", 
            "pitch -1000",
            "flanger 20", 
            "reverb",
            "chorus 0.6 0.9 50 0.4 0.25 2 -t 60 0.32 0.4 1.3 -s", 
            "phaser 0.6 0.66 3 0.6 2 -t")

        panning = (
            "remix 1      2v0.15",
            "remix 1v0.15 2     ",
            "remix 1      2v0.30",
            "remix 1v0.30 2     ",
            )

        ofn = "layer%d.wav" % nr
        soxcmd = "sox %s %s %s %s %s %s %s" % (tr.filename, ofn, trim, panning[nr], fade, delay, random.choice(filters))
        os.system(soxcmd)
        fgmixercmd += ofn + " "
    break
        
fgmixercmd += " fg.wav norm -3"

os.system(fgmixercmd)
comboname = "combo-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
os.system("sox -m bg.wav fg.wav %s" % comboname)
print "%s written, now playing..."
os.system("play -q %s" % comboname)
