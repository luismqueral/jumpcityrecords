import os
import datetime
import bs4
import urllib2
import random

# Grab a few random Wikipedia pagecount files from previous month.

count = 6 # This many files.

# Determine the previous month.
today = datetime.date.today()
year, month = today.year, today.month
month -= 1
if month < 1:
    month = 12
    year -= 1

# Download that months' index file and see which pagecount files are available for download.
baseurl = "http://dumps.wikimedia.org/other/pagecounts-raw/%04d/%04d-%02d/" % (year, year, month)
html = urllib2.urlopen(baseurl).read()
soup = bs4.BeautifulSoup(html)
pagecounturls = []
for a in soup.find_all("a"):
    href = a["href"]
    if href.startswith("pagecounts-"):
        pagecounturls.append(href)
print "Found %d pagecount files for %04d-%02d" % (len(pagecounturls), year, month)

# Choose a few, download them, extract them.
fns = random.sample(pagecounturls, count)
for fn in fns:
    url = baseurl + fn
    os.system("wget " + url)
    os.system("gunzip " + fn)

print "Done! You might want to run 'parse.py' now."

    