#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  distanceCheck.py
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
from motors_cars import carsWith2Motor
from time import sleep

class checkDistanceThread(threading.Thread):
   def __init__(self,distanceChecker, relatedCar:carsWith2Motor):
      threading.Thread.__init__(self)
      self.distanceChecker = distanceChecker
      self.relatedCar = relatedCar
      
   def run(self):
       while True:
           if leaveTheThread:
               break
           if self.distanceChecker.checkIfClose():
               #print("Car too close")
               #self.relatedCar.stop()
               self.relatedCar.forward()
           else:
               pass
                #print("OK")
                
       #self.showLight.doTheShow()
       
class distanceCheck:
        def __init__(self, checkPin,relatedCar):
            self.checkPin = checkPin
            self.distanceCheckSet()
            self.relatedCar = relatedCar
            
        def distanceCheckSet(self):
            GPIO.setup(self.checkPin, GPIO.IN)
 
        def checkIfClose(self):
            return (GPIO.input(self.checkPin) == GPIO.LOW)
            
        def doTheCheckOnThread(self):
            global aThreadRunning
            global leaveTheThread
            try:
                aThreadRunning
                if aThreadRunning.isAlive():
                    return
                else:
                    aThreadRunning.join()
                    del aThreadRunning
            except NameError:
                pass
            aThreadRunning = checkDistanceThread(self,self.relatedCar)
            leaveTheThread = False
            aThreadRunning.start()

        def stopTheCheckThread(self):
            global leaveTheThread
            leaveTheThread = True
        
        def showPinContinous(self):
            while True:
                if self.checkIfClose():
                    print("Too Close")
                else:
                    print ("OK")
                sleep(0.5)
            
                              
def getStandartDistanceChecker(myCar):
    myDistanceChecker = distanceCheck(14, myCar)
    return myDistanceChecker

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
