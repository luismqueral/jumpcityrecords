# -*- coding: utf8 -*-

"""
albumtracks.py

Generate meta-data (name, tracknames, durations etc...) for an album. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import marshal
import codecs
import random
import sys
sys.path.append("..")
import utils
import constants
import datetime


class AlbumTracks(object):
    def __init__(self):
        # The file 'titles.dat' has been prepared by 'parse.py'.
        self.titles = marshal.load(open("titles.dat", "rb"))
        # Divide the titels into english and non-english.
        english_titles = set()
        non_english_titles = set()
        for lang, titleset in self.titles.iteritems():
            if lang == "en":
                english_titles = english_titles.union(self.titles[lang])
            else:
                non_english_titles = non_english_titles.union(self.titles[lang])
        self.english_titles = list(english_titles)
        self.non_english_titles = list(non_english_titles)


    def randomtitle(self, allowparentheses=True):
        while True:
            if utils.rnd(100) < 80:
                name = random.choice(self.english_titles)
            else:
                name = random.choice(self.non_english_titles)
            if not allowparentheses and ("(" in name or ")" in name):
                continue
            return name
            
                
    def generatetrack(self):
        duration = int(random.uniform(constants.TRACKMINDUR, constants.TRACKMAXDUR + 1))
        name = self.randomtitle()
        return name, duration


    def generatealbum(self):
        title = self.randomtitle(False)
        datestamp = datetime.datetime.now().strftime("%Y-%m-%d / %H:%M:%S")
        trackcount = int(random.uniform(constants.MINTRACKSPERALBUM, constants.MAXTRACKSPERALBUM + 1))
        seen = set()
        tracks = []
        while len(tracks) < trackcount:
            candidate = self.generatetrack()
            name, _ = candidate
            if name not in seen: # Avoid duplicate track names.
                tracks.append(candidate)
                seen.add(name)
        return title, datestamp, tracks


    def htmlexample(self):
        ofn = "albumtracks.html"
        with codecs.open(ofn, "w", "utf8") as of:
            of.write(u"""<!DOCTYPE html>
                <html>
                <head>
                    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
                    <style>
                        body {
                            background-color: white;
                            font-family: Monaco, monospace;
                            }
                        td {
                            padding: 0.2em 3em 0.2em 0.2em;
                            }
                        h1 {
                            margin-top: 2em;
                            }
                        div {
                            margin-left: 5em;
                            }
                    </style>
                </head>
                <body><div>\n""");
            for i in xrange(100):
                albumname, datestamp, tracks = self.generatealbum()    
                of.write(u"<h1>%s</h1>\n" % albumname)
                of.write(u"<table>\n")
                for track in tracks:
                    trackname, duration = track
                    minutes = int(duration / 60)
                    seconds = duration - minutes * 60
                    padspace = "&nbsp;" if minutes < 10 else ""
                    of.write(u"<tr><td>%s</td><td>%s%d:%02d</td></tr>" % (trackname, padspace, minutes, seconds))
                of.write(u"</table>\n")
            of.write("</div></body></html>")
        print "'%s' written" % ofn


if __name__ == "__main__":
    a = AlbumTracks()
    a.htmlexample()
