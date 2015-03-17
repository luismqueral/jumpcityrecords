# -*- coding: utf8 -*-

"""
jumpcity.py

Main driver. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import albumart
import albumtracks
import composetrack
import os
import codecs
import constants
import datetime
try:
    import scaup
    scaup_available = True
except ImportError:
    scaup_available = False


def generatealbum():
    """ Generate a complete album. """
    longstring = """\
     ____________        _..._
     | ________ |  ___ .'     `. ____________
     ||        || |   /`.  .-'  \            |
     ||        || |  ( O / O.   "\           |
     ||        || |   | (_)     _/           |
     ||________|| |   /((())) / \_____       |
     |        ] | |   \______/  //    \      |
     |          | |   _..-)    //      \     |
     |          | |  / .\\_..-' \       \    |
     |          | |_/    \       `.      \___|
     |          |  /     |         \     /
_____|__________| /      /         /    / _______
                  |    ./|        /    /
                 _|____\_|        |   /
                 \       /       _)   \__
                  \     /       (_\    \()
               ___|_____|____  / / \\_\/
            __/           |  |/ /___|
    ..'`..'|  |           | _/_/    |       
  .'(( ((( |__|           |(__()    |
.'((( ((( .'__|           |  |______|________
 ((( (( ((`.  |           |  |              /
(((((  (((((`.|           |  |             /
  ((( ((( ((.'|           | /             /
`..-''-....'  |___________|/             /
    """
    print "\n" + longstring
    print "\x1b[1m" + "[ jump city records ]" 
    print " • • • • • • • • • • • • • • • • • • • • • • • • • • • • •"
    # Start with the name and release date.
    at = albumtracks.AlbumTracks()
    while True:
        albumname, datestamp, tracks = at.generatealbum()
        safestamp = datestamp.replace(" / ", " ").replace(":", ".") # Most filesystems don't like / and : in filenames.
        stampedname = u"%s (%s)" % (albumname, safestamp)
        albumdir = os.path.join("..", "_albums", stampedname)
        if os.path.exists(albumdir): # Don't overwrite existing albums with the same name.
            continue
        break
    print "\x1b[1m" + "\x1b[7m" + "\nMaking new album '%s'" % stampedname + "\x1b[0m"
    os.mkdir(albumdir)

    # A nice picture...
    picturefilename = albumart.rendertopng(albumname, datestamp, albumdir)
    
    # Make a description of the entire album - this is added as a comment to every track in the album.
    description = [
        u"░ jump city records, %s" % stampedname,
        u"░ generated by jumpcity.py",
        u"",
        u"░ (https://github.com/luismqueral/jumpcityrecords)",
        u"",
        ]
    maxtracknamelen = max(len(track[0]) for track in tracks)
    for nr, track in enumerate(tracks):
        trackname, duration = track
        minutes = int(duration / 60)
        seconds = duration - minutes * 60
        padspace = " " if minutes < 10 else ""
        line = u"%02d %-*s %s%d:%02d" % (nr + 1, maxtracknamelen, trackname, padspace, minutes, seconds)
        description.append(line)
    description.extend([
        u"a project by:",
        u" • Michiel Overtoom (http://www.michielovertoom.com/)",
        u" • Luis Queral (http://luisquer.al)\n",
        u"view more at: http://soundcloud.com/jumpcityrecords",
        ])
    description = u"\n".join(description)
    descriptionfilename = os.path.join(albumdir, "description.txt")
    with codecs.open(descriptionfilename, "w", "utf8") as of:
        of.write(description)

    # Now compose the actual tracks.
    for nr, track in enumerate(tracks):
        trackname, duration = track
        tags = {
            "ALBUM": albumname,
            "ARTIST": u"[ jump city records ]",
            "DATE": datetime.date.today().isoformat(),
            "TITLE": trackname,
            "DESCRIPTION": descriptionfilename,
            "GENRE": u"Musique Concrète",
            "COMPOSER": u"jumpcity.py",
            "TRACKNUMBER": nr + 1,
            "TRACKTOTAL": len(tracks),    
            }
        # Catch exception and re-generate track in case of error.
        while True:
            try:
                trackfilename = composetrack.generate(duration, albumname, trackname, picturefilename, tags)
            except ValueError, e:
                print "ERROR:", e
                continue
            break
        # Convert problematic characters in filenames, eg. ?, /, \, :, to a space.
        safetrackname = trackname.replace("?", " ").replace("/", " ").replace("\\", " ").replace(":", " ")
        destname = u"%02d %s - %s.%s" % (nr + 1, albumname, safetrackname, constants.OUTPUTFORMAT)
        print "\x1b[92m" + "\x1b[1m" "DESTNAME:" + "\x1b[37m", destname + "\x1b[22m"
        print ""
        print " • • • • • • • • • • • • • • • • • • • • • • • • • • • • •"
        os.rename(trackfilename, os.path.join(albumdir, destname))

    # Clean up
    os.unlink(descriptionfilename)
    print "\x1b[0m"
    return albumdir, albumname

if __name__ == "__main__":
    for i in xrange(1):
        albumdir, albumname = generatealbum()
        print "DEBUG",albumdir, albumname
        if scaup_available:
            scaup.upload(albumname)
