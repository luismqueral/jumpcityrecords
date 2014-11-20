# -*- encoding: utf8 -*-

'''
createprodcastxml.py

Create a RSS (rich site summary) XML file, compatible with iTunes. Software by Michiel Overtoom, motoom@xs4all.nl

TODO: Atom compatibility.

Put the resulting podcast.xml in the www/static directory on the webserver,
the URL then is:

    http://www.jumpcityrecords.com/podcast.xml
    
You can open that URL with a webbrowser, or in iTunes (via File/Subscribe to podcast...)

'''

import os
import glob
import hashlib
import urllib
from lxml import etree as et
import StringIO
import email.Utils
import utils

albumsdir = "../_albums"


nsmap = {
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "atom": "http://www.w3.org/2005/Atom",
    }


def guidfromfile(fn):
    content = open(fn, "rb").read()
    return hashlib.md5(content).hexdigest()


def xml_serialize(node):
    el = et.ElementTree(node)
    output = StringIO.StringIO()
    try:
        el.write(output, encoding=u"UTF-8", xml_declaration=True, pretty_print=True)
    except TypeError:
        el.write(output, encoding=u"UTF-8")  # Early versions of the XML library didn't support the 'xml_declaration' parameter yet.
    xml = output.getvalue()
    return xml


def filesize(fn):
    return os.lstat(fn).st_size
                

def rfc2822date(fn):
    filetime = os.stat(fn).st_mtime        
    return email.Utils.formatdate(filetime, localtime=True)


rss = et.Element(u"rss", version=u"2.0", nsmap=nsmap)
channel = et.SubElement(rss, u"channel")
et.SubElement(channel, u"title").text = u"Jump City Records"
et.SubElement(channel, u"link").text = u"https://github.com/luismqueral/jumpcityrecords" # TODO: make a website at http://www.jumpcityrecords.com
et.SubElement(channel, u"language").text = u"en-us"
et.SubElement(channel, u"copyright").text = u"Jump City Records"
et.SubElement(channel, u"{%s}subtitle" % nsmap["itunes"]).text = u"Jump City Records is an experimental, open-source record label that produces and releases its albums through a series of python bots."
et.SubElement(channel, u"{%s}author" % nsmap["itunes"]).text = u"Jump City Records"
et.SubElement(channel, u"{%s}summary" % nsmap["itunes"]).text = u"Jump City Records is an experimental, open-source record label that produces and releases its albums through a series of pythonic bots."
et.SubElement(channel, u"{%s}description" % nsmap["itunes"]).text = u"Jump City Records is an experimental, open-source record label that produces and releases its albums through a series of python robots."
owner = et.SubElement(rss, u"{%s}owner" % nsmap["itunes"])
et.SubElement(owner, u"name").text = u"Jump City Records" # This shows up in iTunes as the podcast title.
et.SubElement(owner, u"email").text = u"luismqueral@gmail.com"
et.SubElement(channel, u"{%s}image" % nsmap["itunes"]).text = u"http://www.michielovertoom.com/incoming/3uVPrNUc.png" # TODO: Better logo.
et.SubElement(channel, u"{%s}category" % nsmap["itunes"]).text = u"Music"

for albumdir in glob.glob(os.path.join(albumsdir, "*")):
    _, albumname = albumdir.rsplit("/", 1)
    print u"Processing album", albumname
    for songfn in glob.glob(os.path.join(albumdir, "*.mp3")):
        songfn = songfn.decode("utf8")
        _, songname = songfn.rsplit("/", 1)
        urlsongname = urllib.quote_plus(songname.encode("utf8")).replace("+", "%20")
        url = u"http://www.jumpcityrecords.com/albums/%s/%s" % (albumname, urlsongname)
        # Test whether URLs works OK.
        resp = urllib.urlopen(url)
        if resp.code != 200:
            print "Error: '%s' can't be fetched" % url
        item = et.SubElement(channel, u"item")
        et.SubElement(item, u"title").text = songname
        # et.SubElement(item, u"{%s}author" % nsmap["itunes"]).text = u"TODO: John Doe"
        et.SubElement(item, u"{%s}subtitle" % nsmap["itunes"]).text = u"Musique Concrète" # TODO: generated text from YouTube or Google Trends?
        # et.SubElement(item, u"{%s}summary" % nsmap["itunes"]).text = u"TODO: Shown when (i) button is clicked"
        songlength = filesize(songfn)
        et.SubElement(item, u"enclosure", url=url, length=str(songlength), type="audio/mp3")
        guid = guidfromfile(songfn)
        et.SubElement(item, u"guid").text = guid
        et.SubElement(item, u"pubDate").text = rfc2822date(songfn) # TODO: Use track number as seconds value
        success, duration, _ = utils.soundfileduration(songfn)
        et.SubElement(item, u"{%s}duration" % nsmap["itunes"]).text = utils.seconds2hmmss(duration)
        et.SubElement(item, u"{%s}keywords" % nsmap["itunes"]).text = u"Musique Concrète"
        et.SubElement(item, u"{%s}explicit" % nsmap["itunes"]).text = u"yes" # For safety. Title may contain profanity: http://en.wikipedia.org/wiki/Argel_Fucks

with open("podcast.xml", "wt") as of:        
    of.write(xml_serialize(rss))


