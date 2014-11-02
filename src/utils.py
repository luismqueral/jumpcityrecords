
"""
utils.py

Generic routines for the jumpcity project. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import string
import random
import subprocess
import os

def randomname():
    allowed = string.letters + string.digits
    return "".join(random.choice(allowed) for i in xrange(8))


def rnd(v, w=None):
    "Convenience helper for random numbers."
    if w is None:
        return random.uniform(0, v) 
    else:
        return random.uniform(v, w)


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


def execute(cmd):
    """ Execute a command and return its standard output and standard error. """
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return p.communicate()


def soxexecute(cmd):
    """ Execute a SoX command and analyze the error output. Separate the warnings from the errors. """
    output, errors = execute(cmd)
    warnings = []
    realerrors = []
    for line in errors.splitlines():
        if line.startswith("sox FAIL"):
            realerrors.append(line)
        else:
            warnings.append(line)
    if warnings:
        print "SUPPRESSED WARNINGS:", warnings
    return output, "\n".join(realerrors)
    

def soundfileduration(fn):
    """ Use soxi to determine the duration of a sound file, in seconds.
        Return a tuple of (succescode, duration, errormessage). """
    p = subprocess.Popen(("soxi", fn), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = p.communicate()
    if errors:
        return False, None, errors
    for line in output.splitlines():
        if line.startswith("Duration"):
            for part in line.split(" "):
                if "." in part:
                    return True, hhmmss2seconds(part), None
    return False, None, None


if __name__ == "__main__":
    print randomname()

    print rnd(100)

    if os.path.exists("synth-tst.wav"):
        os.unlink("synth-tst.wav")
        
    cmd = "sox -n synth-tst.wav synth 440 fade 0 4"
    out, err = execute(cmd)
    print "out:",out
    print "err:",err

    os.system("ls -al synth-tst.wav")

    cmd = "sox -n synth-tst.wav synth XXX fade 0 4"
    out, err = execute(cmd)
    print "out:",out
    print "err:",err
    
    fn = "../audio/backgrounds/nature/nonexistant"
    print soundfileduration(fn)

    fn = "../audio/backgrounds/nature/ocean.mp3"
    print soundfileduration(fn)

    secs = hhmmss2seconds("01:23:58.230")
    print secs
    print seconds2hhmmss(secs)
