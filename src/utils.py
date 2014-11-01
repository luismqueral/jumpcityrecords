
"""
utils.py

Generic routines for the jumpcity project. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import string
import random
import subprocess

def randomname():
    allowed = string.letters + string.digits
    return "".join(random.choice(allowed) for i in xrange(8))


def rnd(v):
    "Convenience helper for random numbers."
    return random.uniform(0, v) 


def hhmmss2seconds(x):
    "Convert a string like '01:23:58.230' to seconds."
    h, m, s = x.split(":")
    return float(h) * 3600 + float(m) * 60 + float(s)


def seconds2hhmmss(x):
    "Convert a number of seconds (as a float) to a string like '01:23:58.230'."
    left = float(x)
    h = int(left / 3600.0)
    left -= 3600.0 * h
    m = int(left / 60.0)
    left -= 60.0 * m
    s = int(left)
    left -= s
    if left >= 0.001:
        left = int(round(left * 1000))
        return "%02d:%02d:%02d.%03d" % (h, m, s, left)
    else:
        return "%02d:%02d:%02d" % (h, m, s)


def soundfileduration(fn):
    "Use soxi to determine the duration of a sound file, in seconds."
    p = subprocess.Popen(("soxi", fn), stdout=subprocess.PIPE)
    output = p.communicate()[0]
    for line in output.splitlines():
        if line.startswith("Duration"):
            for part in line.split(" "):
                if "." in part:
                    return hhmmss2seconds(part)
    return None


if __name__ == "__main__":
    print randomname()

    print rnd(100)

    fn = "../audio/backgrounds/nature/ocean.mp3"
    print soundfileduration(fn)

    secs = hhmmss2seconds("01:23:58.230")
    print secs
    print seconds2hhmmss(secs)
