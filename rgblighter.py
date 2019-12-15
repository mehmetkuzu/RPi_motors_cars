#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rgblighter.py
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
from random import randint
import time
import _thread
import threading

class showThread(threading.Thread):
   def __init__(self,showLight):
      threading.Thread.__init__(self)
      self.showLight:rgblighter = showLight
   def run(self):
       self.showLight.doTheShow()
       
class rgblighter:
        def __init__(self, rPin,gPin,bPin):
            self.rPin = rPin
            self.gPin = gPin
            self.bPin = bPin
            self.rgblighterSet()
        def rgblighterSet(self):
            GPIO.setup(self.rPin, GPIO.OUT)
            GPIO.output(self.rPin, GPIO.LOW)
            GPIO.setup(self.gPin, GPIO.OUT)
            GPIO.output(self.gPin, GPIO.LOW)
            GPIO.setup(self.bPin, GPIO.OUT)
            GPIO.output(self.bPin, GPIO.LOW)
            self.pR = GPIO.PWM(self.rPin, 1000)
            self.pG = GPIO.PWM(self.gPin, 1000)
            self.pB = GPIO.PWM(self.bPin, 1000)
            self.pR.start(100)
            self.pG.start(100)
            self.pB.start(100)
        def turnOn(self):
            GPIO.output(self.rPin, GPIO.HIGH)
            GPIO.output(self.gPin, GPIO.HIGH)
            GPIO.output(self.bPin, GPIO.HIGH)
        def turnOff(self):
            GPIO.output(self.rPin, GPIO.LOW)
            GPIO.output(self.gPin, GPIO.LOW)
            GPIO.output(self.bPin, GPIO.LOW)
            
        def doTheShowOnThread(self):
            global aThreadRunning
            breakpoint()
            try:
                aThreadRunning
                if aThreadRunning.isAlive():
                    return
                else:
                    aThreadRunning.join()
                    del aThreadRunning
            except NameError:
                pass
            aThreadRunning = showThread(self)
            aThreadRunning.start()
                        
        def doTheShow(self):
            self.turnOn()
            iShow = 100
            while iShow > 0:
                self.pR.ChangeDutyCycle(randint(0,100))
                self.pG.ChangeDutyCycle(randint(0,100))
                self.pB.ChangeDutyCycle(randint(0,100))
                time.sleep(0.10)
                iShow = iShow - 1
            
def getStandartrgblighter():
    myrgblighter = rgblighter(13,6,5)
    return myrgblighter

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
