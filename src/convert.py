
"""
convert.py

Convert audio assests to usable form. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import glob
import os
import sys

if sys.platform.startswith("linux"):
    convtool = "avconv" # Assume system uses libav
else:
    convtool = "ffmpeg"

for dir in glob.glob("../_assets/*"):
    for fn in glob.glob(dir + "/*.m4a"):
        # SoX can't read the 'm4a'. Convert it to flac. 
        print "Converting", fn
        base, ext = fn.rsplit(".", 1)
        source = "%s.m4a" % base
        destination = "%s.flac" % base
        if os.path.exists(destination):
            print "    was already converted"
            continue
        cmd = '%s -v warning -y -i "%s" "%s"' % (convtool, source, destination)       
        os.system(cmd)

# TODO: Also check for mono mp3 files, convert them to stereo. (Note: this used to be a problem, not sure if it still is.)
