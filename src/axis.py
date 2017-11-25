#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import time


class Axis:
    # outer is a ftrobopy(-like) object
    # mot is the number of the motor
    # end is a list of numbers for the end stops
    def __init__(self, outer, mot, end):
        assert(mot in range(1, 5))
        assert(type(end) == list and len(end) >= 1)
        # initialize the main properties
        self.outer = outer
        self.mot = self.outer.motor(mot)
        self.mot.setSpeed(0)
        self.mot.setDistance(0)
        self.speed = 512
        self.initSpeed = 512
        self.direction = 0
        self.distance = 0
        self.initialized = False
        self.pos = 0
        self.maxPos = -1
        # initialize all end stops
        self.end = []
        for e in set(end):
            assert(e in range(1, 9))
            self.end.append(self.outer.input(e))

    def checkAllEndPressed(self):
        # return true if all end stopsare pressed, otherwise false
        for e in self.end:
            if e.state() == 0:
                return(False)
        return(True)

    def initialize(self):
        # initialize the axis
        if not self.checkAllEndPressed():  # initialize only if needed
            self.mot.setSpeed(self.initSpeed)
            while not self.checkAllEndPressed():  # check whether init position is reached
                time.sleep(0.1)
            self.mot.setSpeed(0)
        self.initialized = True
        self.pos = 0

    def posReached(self):
        # check whether the target position is reached
        return(self.mot.finished())

    def goPos(self, pos):
        # move to target position independent of current position
        # check whether target position is in range of axis (if set)
        if self.maxPos != -1:
            assert(pos in range(self.maxPos + 1))
        assert(self.posReached())  # move only if old target position is reached
        # prepare by setting speed and distance to 0
        self.mot.setSpeed(0)
        self.mot.setDistance(0)
        # calculate speed and distance depended on the target position relative to current position
        if pos < self.pos:
            self.distance = self.pos - pos
            self.direction = 1
        elif pos > self.pos:
            self.distance = pos - self.pos
            self.direction = -1
        else:
            self.distance = 0
            self.direction = 0
        # send the values to the motor
        self.mot.setDistance(self.distance)
        self.mot.setSpeed(self.direction * self.speed)
        self.pos = pos  # set current position to new position

    def getCurrentPosition(self):
        # calculate the current position dependeding on the current direction, move distance and target position
        if self.direction == 0:
            return(self.pos)
        elif self.direction == 1:
            return(self.pos + self.distance - self.mot.getCurrentDistance())
        elif self.direction == -1:
            return(self.pos - self.distance + self.mot.getCurrentDistance())
