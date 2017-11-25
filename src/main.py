#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftrobopy import ftrobopy
from axis import *
import time


# initialize controllers
txt = ftrobopy()

# prepare X-Axis
XAxis = Axis(txt, 1, [1, 2])
XAxis.maxPos = 7700
# initialize X-Axis
XAxis.initialize()

# move a bit away from the init position to "present" the X-Axis
XAxis.goPos(2000)
while not XAxis.posReached():
    print(XAxis.getCurrentPosition())
    time.sleep(1)
time.sleep(1)
# move back to 0
XAxis.goPos(0)
while not XAxis.posReached():
    print(XAxis.getCurrentPosition())
    time.sleep(1)
