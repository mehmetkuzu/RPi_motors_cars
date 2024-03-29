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
from motors_cars2 import carsWith2Motor2
from motors_cars2 import getStandartCar2
from motors_cars2 import getStandart4WheelCar2
from laser import laser
from laser import getStandartLaser
from buzzer import buzzer
from buzzer import getStandartBuzzer
from rgblighter import rgblighter
from rgblighter import getStandartrgblighter
from distanceCheck import distanceCheck
from distanceCheck import getStandartDistanceChecker
from arduino_cannon_driver import CannonDriver
from arduino_cannon_driver import getStandartCannonDriver

from general_command_server import GeneralCommandServer
from commander_request_handler import CommandReturns

import RPi.GPIO as GPIO
class CarCommanderFunctionsClass:
    def processCommand(self, commandString):
        global myCar
        global myLaser
        global myBuzzer
        global myRGBLighter
        global myDistanceChecker
        global myCannon
        commandString = commandString.upper()
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
        elif commandString == "QUIT":
            return CommandReturns(False, False, "Shutting down server")
            # Disconnect için bir durum eklenmesi lazım.
        else:
            commandData = commandString.split()
            if len(commandData) < 2:
                return CommandReturns(False, False, "INVALID COMMAND OR COMMAND FORMAT - 1")
            else:
                mainCommand = commandData[0]
                commandParam = commandData[1]
                if mainCommand == "SPEED":
                    try:
                        speed = int(commandParam)
                    except ValueError:
                        return CommandReturns(False, False, "INVALID PARAMETER FOR SPEED")
                    if (speed < 0) or (100 < speed):
                        return CommandReturns(False, False, "INVALID PARAMETER FOR SPEED")
                    else:
                        myCar.setSpeed(speed)
                        return CommandReturns(True,False, "Changing Speed - " + str(speed))
                        
                elif mainCommand == "LEFT":
                    try:
                        angle = int(commandParam)
                    except ValueError:
                        return CommandReturns(False, False, "INVALID PARAMETER FOR LEFT TURN")
                    if (angle < 0) or (angle > 100):
                        return CommandReturns(False, False, "INVALID NUMBER FOR LEFT TURN")
                    else:
                        myCar.setAngle(-angle)
                        return CommandReturns(True,False, "Changing Direction LEFT- " + str(angle))
                elif mainCommand == "RIGHT":
                    try:
                        angle = int(commandParam)
                    except ValueError:
                        return CommandReturns(False, False, "INVALID PARAMETER FOR RIGHT TURN")
                    if (angle < 0) or (angle > 100):
                        return CommandReturns(False, False, "INVALID NUMBER FOR RIGHT TURN")
                    else:
                        myCar.setAngle(angle)
                        return CommandReturns(True,False, "Changing Direction RIGHT- " + str(angle))
                        
                elif mainCommand == "CANNON":
                    if commandParam in {"UP", "DOWN", "LEFT", "RIGHT", "SELECT", "LASER"} :
                        if len(commandData) < 3:
                            myCannon.sendCommand(commandParam + "\n")
                            return CommandReturns(True, False, "CANNON " + commandParam)
                        else:
                            myCannon.sendCommand(commandParam +" " + commandData[2]+ "\n")
                            return CommandReturns(True, False, "CANNON " + commandParam + " " + commandData[2])
                elif mainCommand == "TEST":
                    if commandParam in {"MOTOR"} :
                        if len(commandData) < 3:
                            return CommandReturns(False, False, "MOTOR TO TEST MISSING IN COMMAND")
                        else:
                            try:
                                testMotor = int(commandData[2])
                            except ValueError:
                                return CommandReturns(False, False, "MOTOR INDEX MISFORMULATED TRY 1 2 3 4")
                            if testMotor == 1:
                                myCar.stop()
                                myCar.motorRight.forward()
                                myCar.motorRight.setSpeed(50)
                                return CommandReturns(True, False, "TEST RUNNING - " + commandParam + " " + commandData[2])
                            elif testMotor == 2:
                                myCar.stop()
                                myCar.motorLeft.forward()
                                myCar.motorLeft.setSpeed(50)
                                return CommandReturns(True, False, "TEST RUNNING - " + commandParam + " " + commandData[2])
                            elif testMotor == 3:
                                myCar.stop()
                                myCar.motorRight2.forward()
                                myCar.motorRight2.setSpeed(50)
                                return CommandReturns(True, False, "TEST RUNNING - " + commandParam + " " + commandData[2])
                            elif testMotor == 4:
                                myCar.stop()
                                myCar.motorLeft2.forward()
                                myCar.motorLeft2.setSpeed(50)
                                return CommandReturns(True, False, "TEST RUNNING - " + commandParam + " " + commandData[2])
                            else:
                                return CommandReturns(False, False, "INVALID MOTOR INDEX TRY 1 2 3 4")
                else:
                    return CommandReturns(False, False, "INVALID COMMAND")
            
def DefineTheCar():
    global myCar
    myCar = getStandartCar2()

def Define4WheelTheCar():
    global myCar
    myCar =  getStandart4WheelCar2()

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
    
def DefineTheCannonDriver():
    global myCannon
    myCannon = getStandartCannonDriver()
        
def runCar(): 
    GPIO.setmode(GPIO.BCM)
    DefineTheCar()
    DefineTheLaser()
    DefineTheBuzzer()
    DefineTheRGBLighter()
    DefineTheDistanceChecker()
    commanderFunctions = CarCommanderFunctionsClass()
    myServer = GeneralCommandServer(commanderFunctions, "192.168.0.108", 1700)
    myServer.runTheServer()
    GPIO.cleanup()
    sys.exit(0)

def runCarServer(): 
    GPIO.setmode(GPIO.BCM)
    DefineTheCar()
    DefineTheLaser()
    DefineTheBuzzer()
    DefineTheRGBLighter()
    DefineTheDistanceChecker()
    DefineTheCannonDriver()
    commanderFunctions = CarCommanderFunctionsClass()
    
    host = "0.0.0.0"
    port = 1700
    
    myServer = GeneralCommandServer(commanderFunctions, host, port)
    myServer.runTheServer()
    GPIO.cleanup()
    sys.exit(0)

def runCarServerWith4Motors(): 
    GPIO.setmode(GPIO.BCM)
    Define4WheelTheCar()
    DefineTheLaser()
    DefineTheBuzzer()
    DefineTheRGBLighter()
    DefineTheDistanceChecker()
    DefineTheCannonDriver()
    commanderFunctions = CarCommanderFunctionsClass()
    
    host = "0.0.0.0"
    port = 1700
    
    myServer = GeneralCommandServer(commanderFunctions, host, port)
    myServer.runTheServer()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    runCarServerWith4Motors()
