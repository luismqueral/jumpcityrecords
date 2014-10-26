
"""
jumpcity.py

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
    fn = "/Users/user/Desktop/jumpcityrecords-audio/backgrounds/nature/Madacy - Earth sounds - Ocean surf.mp3"
    print soundfileduration(fn)
