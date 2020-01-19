#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  usb_camera.py
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

import cv2

def testCamera():
	 
	# initialize the camera
	cam = cv2.VideoCapture(0)
	ret, image = cam.read()

	if ret:
		cv2.imshow('SnapshotTest',image)
		cv2.waitKey(0)
		cv2.destroyWindow('SnapshotTest')
		cv2.imwrite('/home/pi/book/output/SnapshotTest.jpg',image)
	cam.release()

def main(args):
	testCamera()

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
