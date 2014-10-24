
"""
jumpcity.py

Generic routines for the jumpcity project. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import string
import random

def randomname():
    allowed = string.letters + string.digits
    return "".join(random.choice(allowed) for i in xrange(8))


def rnd(v):
    "Convenience helper for random numbers."
    return random.uniform(0, v) 


if __name__ == "__main__":
    print randomname()
    print rnd(100)
