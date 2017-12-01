#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

__all__ = ['LinearLine']

"""
|=======|
|y=m*x+n|
|=======|

y=m*x+n | -n
y-n=m*x | :m
==> x=(y-n)/m

m=(y0-y1)/(x0-x1)

y=m*x+n | -m*x
==> n=y-m*x
"""


class LinearLine:
    # look at the long string above for the description!
    def __init__(self, point0, point1):
        x0, y0 = point0
        x1, y1 = point1
        assert(x0 != x1)
        self.m = (y0 - y1) / (x0 - x1)
        self.n = y0 - self.m * x0

    def getPoint(self, x=None, y=None):
        assert(not (x == None and y == None))
        if x != None and y != None:
            assert(y == self.m * x + self.n)
            return(x, y)
        if x != None:
            return(x, self.m * x + self.n)
        if y != None:
            return((y - self.n) / self.m, y)
