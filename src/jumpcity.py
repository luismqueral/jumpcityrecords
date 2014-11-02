
"""
jumpcity.py

Main driver. Software by Michiel Overtoom, motoom@xs4all.nl
"""

# import albumart
import albumtracks
import composetrack
import utils
import os


def generatealbum():
    """ Generate a complete album. """
    at = albumtracks.AlbumTracks()
    while True:
        name, tracks = at.generatealbum()
        albumdir = os.path.join("..", "_albums", name)
        if os.path.exists(albumdir): # Don't overwrite existing albums with the same name.
            continue
        break
    print "Making new album '%s'" % name
    os.mkdir(albumdir)
    for track in tracks:
        trackname, duration = track
        trackfilename = composetrack.generate(duration, mp3=True)
        os.rename(trackfilename, os.path.join(albumdir, trackname + ".mp3"))


if __name__ == "__main__":
    for i in xrange(5):
        name = generatealbum()
