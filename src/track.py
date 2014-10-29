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

MINDUR = 15 # Minumum duration of mix.
MAXDUR = 15 * 60 # Maximum duration of mix.

def generate(mp3=True, play=False):
    targetduration = int(random.uniform(MINDUR, MAXDUR))

    asset = random.choice([name for name in glob.glob("../_assets/*") if os.path.isdir(name)])
    asset = "../_assets/Axisem083_8" # TEST: Manual override.
    print "Creating a track from '%s' asset, target duration %s" % (asset, jumpcity.seconds2hhmmss(targetduration))
    fns = glob.glob(os.path.join(asset, "*"))

    mixercmd = "sox -m "
    for nr, fn in enumerate(random.sample(fns, 3)):
        # See how long the sample is.
        fndur = jumpcity.soundfileduration(fn)
        print "    Source for layer%d: %s (duration %s)" % (nr, fn, jumpcity.seconds2hhmmss(fndur))
        # If sample duration is longer than 'targetduration' seconds, fade it out.
        fade = ""
        if fndur > targetduration:
            fade = "fade 0 %d 4" % targetduration
            print "    ...fading to: %s" % fade
        # If it is shorter than the target duration, repeat it.
        repeat = ""
        if fndur < targetduration:
            repeats = (targetduration - fndur) / fndur
            repeat = "repeat %d" % repeats
            print "    ...repeating, extra %d times (for a total duration of %s)" % (repeats, (repeats + 1) * fndur)
        panning = (
            "remix 1 2", # No panning for sample #1
            "remix 1 2v0.25", # Right panning for sample #2
            "remix 1v0.25 2", # Left panning for sample #3
            )
        layerfn = "layer%d.wav" % nr
        cmd = 'sox "%s" "%s" %s %s %s' % (fn, layerfn, panning[nr], repeat, fade)
        os.system(cmd)    
        print "    ...resulting duration: %s" % jumpcity.seconds2hhmmss(jumpcity.soundfileduration(layerfn))
        mixercmd += '"%s" ' % layerfn

    trackname = "track-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
    mixercmd += trackname
    print "Mixing to %s..." % trackname, 
    os.system(mixercmd)
    print "done"

    os.system("rm layer*.wav") # Remove tempfiles.

    if play:
        os.system("play -q %s" % trackname)

    if mp3:
        print "Making mp3..."
        os.system("lame %s" % trackname)
        os.unlink(trackname)


if __name__ == "__main__":
    for i in xrange(20):
        generate()
        