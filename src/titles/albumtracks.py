import marshal
import codecs
import random
import sys
sys.path.append("..")
import jumpcity

titles = marshal.load(open("titles.dat", "rb"))

# Divide the titels into englisg and non-english.
english_titles = set()
non_english_titles = set()
for lang, titleset in titles.iteritems():
    if lang == "en":
        english_titles = english_titles.union(titles[lang])
    else:
        non_english_titles = non_english_titles.union(titles[lang])
english_titles = list(english_titles)
non_english_titles = list(non_english_titles)


def generatetrack():
    duration = int(random.uniform(15, 60 * 15))
    if jumpcity.rnd(100) < 80:
        name = random.choice(english_titles)
    else:
        name = random.choice(non_english_titles)
    return name, duration


def generatealbum():
    title = jumpcity.randomname()
    trackcount = int(random.uniform(3, 24))
    seen = set() 
    tracks = []
    while len(tracks) < trackcount:
        candidate = generatetrack()
        name, _ = candidate
        if name not in seen: # Avoid duplicate track names.
            tracks.append(candidate)
            seen.add(name)
    return title, tracks


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
        albumname, tracks = generatealbum()    
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
