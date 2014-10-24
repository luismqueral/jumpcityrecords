
"""
rotate.py

2D rotation and proximity routines. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import math
import collections

Point = collections.namedtuple("Point", "x y")
Rectangle = collections.namedtuple("Rectangle", "a b c d")


def barycenter(rect):
    "Return the center of a rectangle."
    totx, toty = 0.0, 0.0
    for p in rect:
        totx += p.x
        toty += p.y
    return Point(totx / 4.0, toty / 4.0)


def rotatedpoint(p, center, deg):
    """Return a new rotated point by rotating point 'p' around point 'center' for 'deg' degrees.
    Positive degrees turn anti-clockwise (todo: test if this is so)"""
    rad = math.radians(deg)
    c = math.cos(rad)
    s = math.sin(rad)
    x, y = p.x - center.x, p.y - center.y
    x, y = x * c - y * s, x * s + y * c
    x, y = x + center.x, y + center.y
    return Point(x, y)


def rotatedrectangle(r, deg):
    "Return a new rotated rectangle by rotating rectangle 'r' around its center for 'deg' degrees."
    center = barycenter(r)
    newp = []
    for p in r:
        newp.append(rotatedpoint(p, center, deg))
    return Rectangle(*newp)


def pointtolinesegment(p0, p1, p2):
    "Return the distance of point p0 to the line segment p1...p2"
    # TODO
    raise NotImplementedError


def overlap(r1, r2):
    "Return True if rectangles r1 and r2 overlap"
    # TODO
    return False


def nearby(r1, r2, distance):
    "Return True if any point of r1 is closer than distance to any line segment of rectangle r2"
    # TODO
    return False


if __name__ == "__main__":
    r = Rectangle(Point(-2, -2), Point(-2, 2), Point(2, 2), Point(2, -2))
    assert barycenter(r) == Point(0, 0)

    rr = rotatedrectangle(r, 5)
    print rr
