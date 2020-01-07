import sys
import socket 
import socketserver
import abc
import threading
import _thread
from time import sleep
#from socketserver import ThreadingMixIn 
from socketserver import StreamRequestHandler
from socketserver import BaseRequestHandler
from socketserver import TCPServer
from datetime import datetime
from motors_cars import carsWith2Motor
from motors_cars import getStandartCar
from laser import laser
from laser import getStandartLaser
from buzzer import buzzer
from buzzer import getStandartBuzzer
from rgblighter import rgblighter
from rgblighter import getStandartrgblighter
from distanceCheck import distanceCheck
from distanceCheck import getStandartDistanceChecker

from general_command_server import GeneralCommandServer

import RPi.GPIO as GPIO
class CarCommanderFunctionsClass:
    def processCommand(self, commandString):
        global myCar
        global myLaser
        global myBuzzer
        global myRGBLighter
        global myDistanceChecker
        if commandString == "FORWARD":
            myCar.forward()
            return CommandReturns(True,False, "GOING FORWARD")
        elif commandString == "BACKWARD":
            myCar.backward()
            return CommandReturns(True,False, "GOING BACKWARD")
        elif commandString == "STOP":
            myCar.stop()
            return CommandReturns(True,False, "STOPPED")
        elif commandString == "KILL":
            myCar.stop()
            return CommandReturns(True,True, "Shutting down server")
        else:
			return CommandReturns(False, False, "INVALID COMMAND OR COMMAND FORMAT")
			
class CarCommandServer:
    def __init__(self, commanderFunctions):
        self.commanderFunctions = commanderFunctions

    def runTheServer(self): 
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = "localhost", 1700
        #server = TCPServer((HOST, PORT), ThreadedTCPRequestHandlerSample)
        server = None
        try:
            server = TCPServer((HOST, PORT), CommanderRequestHandler)
            #socketserver.TCPServer.allow_reuse_address = True
            server.allow_reuse_address = True
            server.timeout = 5
            server.commanderFunctions = self.commanderFunctions
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        # except Exception:
            # if server:
                # server.shutdown()
        if server:
            server.shutdown()			
    
    def DefineTheCar():
        global myCar
        myCar = getStandartCar()
    
    def DefineTheLaser():
        global myLaser
        myLaser = getStandartLaser()
        
    def DefineTheBuzzer():
        global myBuzzer
        myBuzzer = getStandartBuzzer()

    def DefineTheBuzzer():
        global myBuzzer
        myBuzzer = getStandartBuzzer()
        
    def DefineTheRGBLighter():
        global myRGBLighter
        myRGBLighter = getStandartrgblighter()
        
    def DefineTheDistanceChecker():
        global myDistanceChecker
        global myCar
        myDistanceChecker = getStandartDistanceChecker(myCar)
        
def runCar(): 
    GPIO.setmode(GPIO.BCM)
    CarCommandServer.DefineTheCar()
    CarCommandServer.DefineTheLaser()
    CarCommandServer.DefineTheBuzzer()
    CarCommandServer.DefineTheRGBLighter()
    CarCommandServer.DefineTheDistanceChecker()
    commanderFunctions = CarCommanderFunctionsClass()
    myServer = CarCommandServer(commanderFunctions)
    myServer.runTheServer()
    GPIO.cleanup()
    sys.exit(0)
if __name__ == "__main__":
    runCar()
