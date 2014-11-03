
"""
jumpcity.py

Main driver. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import albumart
import albumtracks
import composetrack
import utils
import os
import codecs
import constants

def generatealbum():
    """ Generate a complete album. """
    at = albumtracks.AlbumTracks()
    while True:
        albumname, tracks = at.generatealbum()
        albumdir = os.path.join("..", "_albums", albumname)
        if os.path.exists(albumdir): # Don't overwrite existing albums with the same name.
            continue
        break
    print "\nMaking new album '%s'" % albumname
    os.mkdir(albumdir)

    albumart.rendertopng(albumname, albumdir)
    
    readme = []
    maxtracknamelen = max(len(track[0]) for track in tracks)
    for nr, track in enumerate(tracks):
        trackname, duration = track
        # Catch exception and re-generate track in case of error.
        while True:
            try:
                trackfilename = composetrack.generate(duration, albumname, trackname)
            except ValueError:
                continue
            break
        # TODO: What about problematic characters in filenames, eg. ?, /, \, :
        destname = u"%02d %s - %s.%s" % (nr + 1, albumname, trackname, constants.OUTPUTFORMAT)
        print "DESTNAME:", destname
        os.rename(trackfilename, os.path.join(albumdir, destname))
        # An entry in the readme.
        minutes = int(duration / 60)
        seconds = duration - minutes * 60
        padspace = " " if minutes < 10 else ""
        line = u"%02d %-*s %s%d:%02d" % (nr + 1, maxtracknamelen, trackname, padspace, minutes, seconds)
        readme.append(line)
    readme = u"\n".join(readme)
    with codecs.open(os.path.join(albumdir, "readme.md"), "w", "utf8") as of:
        of.write(readme)


if __name__ == "__main__":
    for i in xrange(5):
        name = generatealbum()
