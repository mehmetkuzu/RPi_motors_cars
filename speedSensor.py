#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  speedSensor.py
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
#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import time, math
from collections import deque

dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 25                                              
pulse = 0
start_timer = time.time()

class speedSensor:
        def __init__(self, speedPin, ,r_cm,holeCount, speedWindow):
            self.speedPin = speedPin
            self.speedWindow = speedWindow
            self.circ_cm = (2*math.pi)*r_cm          # calculate wheel circumference in CM
            self.holeCount = holeCount
            self.speedSensorSet()
            
        def speedSensorSet(self):
			GPIO.setup(self.speedPin,GPIO.IN,GPIO.PUD_UP)
		def turnOnDetector(self):
			GPIO.remove_event_detect(self.speedPin)
			self.pulse = 0
			self.windowTimers = deque()
			self.start_timer = time.time()
			GPIO.add_event_detect(self.speedPin, GPIO.FALLING, callback = calculate_elapse, bouncetime = 20)
		def turnOffDetector(self):
			GPIO.remove_event_detect(self.speedPin)
			self.pulse = 0
			self.windowTimers.clear()
		def calculate_elapse(channel):              # callback function
			self.pulse += 1     
			self.elapse = time.time() - self.start_timer      # elapse for every 1 complete rotation made!
			if len(self.windowTimers) == self.speedWindow:
				self.windowTimers.popleft()
			self.windowTimers.append(time.time())
			self.start_timer = time.time()               # let current time equals to start_timer
		def calculate_speed(self):
			if self.elapse != 0:
				rpm = ((1/self.elapse) * 60))/self.holeCount
			return (self.circ_cm * rpm)/100000 # convert cm to km
		def calculate_speed_inwindow(self):
			timerCount = len(self.windowTimers)
			if timerCount < 2:
				return(self.calculate(r_cm))
			firstTime = self.windowTimers.popleft()
			lastTime = self.windowTimers.pop()
			self.windowTimers.appendleft(firstTime)
			self.windowTimers.append(lastTime)
			secondsPassed = lastTime - firstTime
			rpm = (((timerCount-1)/secondsPassed)) * 60)/self.holeCount
			return (self.circ_cm * rpm)/100000 # convert cm to km
