#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  buzzer.py
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

class buzzer:
        def __init__(self, buzzerPin):
            self.buzzerPin = buzzerPin
        def buzzerSet(self):
            GPIO.setup(self.buzzerPin, GPIO.OUT)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        def turnOn(self):
            GPIO.output(self.buzzerPin, GPIO.HIGH)
        def turnOff(self):
            GPIO.output(self.buzzerPin, GPIO.LOW)
            
def getStandartBuzzer():
    mybuzzer = buzzer(19)
    mybuzzer.buzzerSet()
    return mybuzzer

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
