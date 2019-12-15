#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  laser_test.py
#  
#  Copyright 2019  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import RPi.GPIO as GPIO
import time

class laser:
        def __init__(self, laserPin):
            self.laserPin = laserPin
        def laserSet(self):
            GPIO.setup(self.laserPin, GPIO.OUT)
            GPIO.output(self.laserPin, GPIO.LOW)
        def turnOn(self):
            GPIO.output(self.laserPin, GPIO.HIGH)
        def turnOff(self):
            GPIO.output(self.laserPin, GPIO.LOW)
            
def getStandartLaser():
    myLaser = laser(16)
    myLaser.laserSet()
    return myLaser
            
def main(args):
    testMe()
    
def testMe():
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(16, GPIO.OUT)
    GPIO.output(16,GPIO.HIGH) 
    time.sleep(3) 
    GPIO.output(16,GPIO.LOW) 
    time.sleep(1) 

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
