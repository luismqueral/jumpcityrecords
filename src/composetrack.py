# -*- coding: utf8 -*-

import os
import random
import glob
import utils
import datetime
import constants

""" Create a track from random assets. Software by Michiel Overtoom, motoom@xs4all.nl

- Choose a random directory from the _assets subdirectory.
- Choose three random files in this subdirectory.
- Mix them.

Return the name of the generated track.

TODO: determine (and correct) bitrate. SoX won't mix soundfiles with different bitrates.
"""


def generate(targetduration=None, albumname=None, trackname=None, picturefilename=None, play=False):
    """ Generate one album track. """
    if targetduration is None:
        targetduration = int(random.uniform(constants.TRACKMINDUR, constants.TRACKMAXDUR))

    asset = random.choice([name for name in glob.glob("../_assets/*") if os.path.isdir(name)])
    print "Creating a track from '%s' asset, target duration %s" % (asset, utils.seconds2hhmmss(targetduration))
    fns = [fn for fn in glob.glob(os.path.join(asset, "*")) if not fn.endswith(".m4a")]

    mixercmd = "sox -m "
    for nr, fn in enumerate(random.sample(fns, 3)):
        # See how long the sample is.
        success, fndur, errors = utils.soundfileduration(fn)
        if not success:
            raise ValueError("generate() can't determine the duration of '%s': %s" % (filename, errors))
        print "    Source for layer%d: %s (duration %s)" % (nr, fn, utils.seconds2hhmmss(fndur))
        # If sample duration is longer than 'targetduration' seconds, select a random fragment from it, and fade it out.
        fade = trim = ""
        if fndur > targetduration:
            trimstart = random.uniform(0, max(0, (fndur - targetduration - 4)))
            trimlength = targetduration
            trim = "trim %d %d" % (trimstart, trimlength)
            print "    ...excerpt from %s to %s (duration %s)" % (utils.seconds2hhmmss(trimstart), utils.seconds2hhmmss(trimstart + trimlength), utils.seconds2hhmmss(trimlength))
            fade = "fade 0 %d 4" % targetduration
            print "    ...fade: %s" % fade
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
        cmd = 'sox "%s" "%s" channels 2 rate 44100 %s %s %s %s' % (fn, layerfn, panning[nr], repeat, trim, fade)
        _, errors = utils.soxexecute(cmd)
        if errors:
            raise ValueError("generate() can't create layer '%s': %s" % (layerfn, errors))   
        result, layerdur, errors = utils.soundfileduration(layerfn)
        if errors:
            raise ValueError("generate() can't determine duration of '%s': %s" % (layerfn, errors))   
        print "    ...resulting duration: %s" % utils.seconds2hhmmss(layerdur)
        mixercmd += '"%s" ' % layerfn

    trackfilename = "track-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
    mixercmd += trackfilename
    print "Mixing to %s..." % trackfilename, 
    _, errors = utils.soxexecute(mixercmd)
    if errors:
        raise ValueError("generate() can't mix: %s" % (trackfilename, errors))   
    print "done"

    os.system("rm layer*.wav") # Remove tempfiles.

    if play:
        os.system("play -q %s" % trackfilename)

    if constants.OUTPUTFORMAT == "mp3":
        print "Making mp3..."
        id3tags = ' --ta "Jumpcity Records" --ty %04d' % datetime.date.today().year
        if albumname:
            id3tags += ' --tl "%s"' % albumname
        if trackname:
            id3tags += ' --tt "%s"' % trackname
        res = os.system("lame %s %s" % (id3tags, trackfilename))
        if res != 0:
            print "LAME error %d" % res
            return None
        os.unlink(trackfilename)
        trackfilename = trackfilename.replace(".wav", ".mp3")
    elif constants.OUTPUTFORMAT == "flac":
        print "Making flac..."
        pictureclause = ""
        if picturefilename:
            pictureclause = '--picture="%s" ' % picturefilename
        cmd = 'flac -s -f -8 --delete-input-file %s "%s"' % (pictureclause, trackfilename)
        print "SYSTEM:", cmd
        res = os.system(cmd)
        if res != 0:
            print "flac error %d" % res
            return None
        trackfilename = trackfilename.replace(".wav", ".flac")
    else:
        raise Exception("Unrecognized output format '%s'" % constants.OUTPUTFORMAT)
    return trackfilename
    
    

if __name__ == "__main__":
    for i in xrange(20):
        generate()
