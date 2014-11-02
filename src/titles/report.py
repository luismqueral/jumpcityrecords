
"""
Load the titles that 'parse.py' saved, and produces a report.
"""

import marshal
import codecs

titles = marshal.load(open("../titles.dat", "rb"))

textreport = False
htmlreport = True

if textreport:
    print sorted(titles.keys(), key=lambda x: x.lower())
    for lang in sorted(titles.keys(), key=lambda x: x.lower()):
        titleset = titles[lang]
        print
        print lang
        nr = 100
        for title in titleset:
            print "   ", title
            nr -= 1
            if nr == 0:
                break

if htmlreport:
    ofn = "titles-report.html"
    with codecs.open(ofn, "w", "utf8") as of:
        of.write(u'<!DOCTYPE html>\n<html><head><meta http-equiv="content-type" content="text/html; charset=utf-8" /></head><body>\n')
        for lang in sorted(titles.keys(), key=lambda x: x.lower()):
            titleset = titles[lang]
            of.write(u"<h2>%s</h2>\n" % lang)
            nr = 100
            for title in titleset:
                of.write(u"%s<br>" % title)
                nr -= 1
                if nr == 0:
                    break        
        of.write("</body></html>")
    print "'%s' written" % ofn
