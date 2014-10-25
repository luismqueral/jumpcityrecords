
"Processes downloaded files like 'pagecounts-20140917-080000' and isolates the Wikipedia article titles from them."

import glob
import urllib2
import collections
import time
import marshal
import random
import re

# Don't read titles from these projects.
forbiddenprojects = set(("Www","am", "AR", "ar", "arc", "arz", "as", "bh", "bn", "bo", "bpy", "chr",
    "ckb", "cr"))

# TODO: Maybe it's better to specify what languages (=projects) to include.


titles = collections.defaultdict(set) # Mapping from language -> set of titles

errors = successes = 0
for fn in glob.glob("pagecounts-????????-??????"):
    print "Processing", fn
    for line in open(fn):
        line = urllib2.unquote(line.strip()).replace("_", " ")
        try:
            line = line.decode("utf8")
        except UnicodeDecodeError:
            errors += 1
            continue
        project, rest = line.split(" ", 1)
        if project in forbiddenprojects:
            continue
        if "." in project:
            continue # Only pageviews of articles.
        if len(rest) < 5 or len(rest) > 40:
            continue # Check for minimum and maximum length.
        if rest[0].isdigit():
            continue # No numeric titles.
        if rest.startswith((".", "%")):
            continue # No titles that start with a dot or a percent sign.
        if ":" in rest:
            continue # No special pages.
        if "\\" in rest:
            continue # Distrust titles with backslashes in them.
        title, _, _ = rest.rsplit(" ", 2)
        titles[project].add(title)
        successes += 1

if errors:
    print "%s titles extracted; %d utf8 decoding errors" % (successes, errors)
    
marshal.dump(dict(titles), open("titles.dat", "wb"), 2)
