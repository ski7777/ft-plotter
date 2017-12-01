#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

from ftrobopy import ftrobopy
from CAxis import *
from CLinearLine import *
import time

__all__ = ['Plotter']


linearMaxStep = 50


class Plotter:
    def __init__(self):
        # initialize controllers
        self.txt = ftrobopy()

        # prepare X-Axis
        self.XAxis = Axis(self.txt, 1, [1, 2])
        self.XAxis.maxPos = 7700

        # prepare Y-Axis
        self.YAxis = Axis(self.txt, 2, [3])  # not built yet...
        #self.YAxis.maxPos = 7700

        # initialize X-Axis
        self.XAxis.initialize()
        # self.XAxis.startWatchdog() # watchdogs disabled due some stucks caused by software

        # initialize Y-Axis
        self.YAxis.initialize()
        # self.YAxis.startWatchdog()

        self.__posX = 0
        self.__posY = 0

    @property
    def posX(self):
        return(self.__posX)

    @property
    def posY(self):
        return(self.__posY)

    def moveDirect(self, x, y):
        assert(type(x) == int and type(y) == int)
        self.XAxis.goPos(x)
        self.YAxis.goPos(y)
        while not self.XAxis.posReached():
            pass
        while not self.YAxis.posReached():
            pass
        self.__posX = x
        self.__posY = y

    def roundPoint(self, point):
        # rount point and convert to int
        return(int(round(point[0])), int(round(point[1])))

    def moveLinear(self, x, y):
        # check whether we need to move, otherwise exit
        if self.posX == x and self.posY == y:
            return
        # check whether we onlx need to move one axis. Exit when finished
        # do this for the X-Axis
        if self.posX == x:
            self.moveDirect(x, y)
            return
        # do this for the Y-Axis
        if self.posY == y:
            self.moveDirect(x, y)
            return
        # we need to move both axis
        # check which axis needs to be moved further (direction) and set the step size and start and stop value
        # invert step size if we move in nagative direction
        if abs(self.posX - x) > abs(self.posY - y):
            # X-Axis needs to be moved further
            step = linearMaxStep  # maximum range between two x coordinates
            start = self.posX  # x value start
            stop = x  # x xalue stop
            direction = 0  # direction (x/y) -> x
            if self.posX > x:
                step = -step
        else:
            # Y-Axis needs to be moved further
            yStep = linearMaxStep  # maximum range between two y coordinates
            start = self.posY  # y value start
            stop = y  # y xalue stop
            direction = 1  # direction (x/y) -> y
            if self.posY > y:
                step = -step
        # create linear line object
        line = LinearLine((self.posX, self.posY), (x, y))
        points = []
        # calculate the points
        for z in list(range(start, stop, step)) + [stop]:
            if direction == 0:
                points.append(line.getPoint(x=z))
            elif direction == 1:
                points.append(line.getPoint(y=z))
        # move to the points
        for xp, yp in points:
            xp, yp = self.roundPoint((xp, yp))
            print(xp, yp)
            self.moveDirect(xp, yp)
