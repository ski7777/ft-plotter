#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#

import time
from _thread import start_new_thread


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
        self.wdInterval = 0.1
        self.wdStrikeTime = 2
        self.wdMinMoveAlertReset = 20
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
            self.mot.setSpeed(-self.initSpeed)
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
            self.direction = -1
        elif pos > self.pos:
            self.distance = pos - self.pos
            self.direction = 1
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
        elif self.direction == -1:
            return(self.pos + self.distance - self.mot.getCurrentDistance())
        elif self.direction == 1:
            return(self.pos - self.distance + self.mot.getCurrentDistance())

    def watchdog(self):
        # watchdogthread to monitor the motor and restart it in case of stuck
        # initialize variables
        # saves the last seen position, if pos is reached, set to 0
        lastPos = 0
        # saves the time of stuck, 0 if moving/pos reached
        motStop = 0
        while True:
            start = time.time()  # save start time of round
            if not self.posReached():  # execute only if target position is not reached
                if lastPos == self.mot.getCurrentDistance():  # detect a stucking motor
                    if motStop == 0:
                        # set time of stuck if this was the first time we detected a stucking motor
                        motStop = time.time()
                else:
                    # motor is runnig :) Save this!
                    motStop = 0
                if motStop != 0 and motStop + self.wdStrikeTime < time.time():
                    # detect that the motor is stuckig for a longer time
                    # reanimate the motor until it is runnig ;-)
                    while lastPos + self.wdMinMoveAlertReset > self.mot.getCurrentDistance():
                        # stop the motor for a moment and restart it
                        self.mot.setSpeed(0)
                        time.sleep(1)
                        self.mot.setSpeed(self.direction * self.speed)
                        time.sleep(4)
                    motStop = 0  # motor is runnig :) Save this!
                lastPos = self.mot.getCurrentDistance()  # save the last moving position
            else:
                lastPos = 0  # reset last moving position
            # wait until nex round starts
            if self.wdInterval > time.time() - start:
                time.sleep(self.wdInterval - time.time() + start)

    def startWatchdog(self):
        # start the watchdog
        start_new_thread(self.watchdog, ())
