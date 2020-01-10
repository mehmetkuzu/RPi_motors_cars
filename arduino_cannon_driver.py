#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  arduino_cannon_driver.py
#  
#  Copyright 2020 mkz <mkz@mkVostroUbn>
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
import serial
import time
def testUSB():
    port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=3.0)
    i = 0
    while i< 8:
        port.write("UP\n".encode())
        i += 1
        #rcv = port.read(10)
        #print (rcv)
        time.sleep(1)
        #port.write("\r\nYou sent:" + repr(rcv))

def main(args):
    testUSB()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
