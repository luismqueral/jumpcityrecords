# -*- coding: utf8 -*-

"""
composetrack.py

Create a track from random assets. Software by Michiel Overtoom, motoom@xs4all.nl

- Choose a random directory from the _assets subdirectory.
- Choose three random files in this subdirectory.
- Mix them.

Return the name of the generated track.

TODO: determine (and correct) bitrate. SoX won't mix soundfiles with different bitrates.
"""

import os
import random
import glob
import utils
import datetime
import constants


def generate(targetduration=None, albumname=None, trackname=None, picturefilename=None, tags=None, play=False):
    """ Generate one album track. """
    if targetduration is None:
        targetduration = int(random.uniform(constants.TRACKMINDUR, constants.TRACKMAXDUR))

    asset = random.choice([name for name in glob.glob("../_assets/*") if os.path.isdir(name)])
    print "\x1b[36m" + "\x1b[1m" + "\n Creating a track from '%s' asset, target duration %s \n" % (asset, utils.seconds2hhmmss(targetduration)) + "\x1b[22m" + "\x1b[37m"
    fns = [fn for fn in glob.glob(os.path.join(asset, "*")) if not fn.endswith(".m4a")]

    mixercmd = "sox -m "
    for nr, fn in enumerate(random.sample(fns, 3)):
        # See how long the sample is.
        success, fndur, errors = utils.soundfileduration(fn)
        if not success:
            raise ValueError("generate() can't determine the duration of '%s': %s" % (fn, errors))
        print "\x1b[1m" + "    Source for layer%d: %s (duration %s)" % (nr, fn, utils.seconds2hhmmss(fndur)) + "\x1b[22m"
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
        print "    ...resulting duration: %s \n" % utils.seconds2hhmmss(layerdur)
        mixercmd += '"%s" ' % layerfn

    trackfilename = "track-%s.wav" % datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
    mixercmd += trackfilename
    print "Mixing to %s..." % trackfilename, 
    _, errors = utils.soxexecute(mixercmd)
    if errors:
        raise ValueError("generate() can't mix: %s" % (trackfilename, errors))   
    print ""
    print "\x1b[92m" + "\x1b[1m" + "done" + "\x1b[22m" + "\x1b[37m"

    os.system("rm layer*.wav") # Remove tempfiles.

    if play:
        os.system("play -q %s" % trackfilename)

    if constants.OUTPUTFORMAT == "mp3":
        print ""
        print "Making mp3..."
        id3tags = u' --ta "Jump City Records" --ty %04d' % datetime.date.today().year
        if albumname:
            id3tags += u' --tl "%s"' % albumname
        if trackname:
            id3tags += u' --tt "%s"' % trackname
        cmd = u"lame %s %s" % (id3tags, trackfilename)
        res = os.system(cmd.encode("utf8"))
        if res != 0:
            print "LAME error %d" % res
            return None
        os.unlink(trackfilename)
        trackfilename = trackfilename.replace(u".wav", u".mp3")
    elif constants.OUTPUTFORMAT == "flac":
        print ""
        print "Making flac..."
        pictureclause = u""
        if picturefilename:
            pictureclause = u'--picture="%s" ' % picturefilename
        tagclause = u""
        if tags:
            for field, value in tags.iteritems():
                if field == "DESCRIPTION":
                    tagclause += u'--tag-from-file=%s="%s" ' % (field, value)
                else:
                    tagclause += u'--tag=%s="%s" ' % (field, value)                    
        cmd = u'flac -s -f -8 --delete-input-file %s %s "%s"' % (pictureclause, tagclause, trackfilename)
        res = os.system(cmd.encode("utf8"))
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
