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


import RPi.GPIO as GPIO

class CommandProcessor:
    @abc.abstractmethod 
    def processCommand(self,command):
        pass
        
class sampleCommandProcessor(CommandProcessor):
    def processCommand(command:str):
        if command == "END":
            return "END"
        else:
            return "SampleOlayı"

class CarCommanderRequestHandler(StreamRequestHandler):
    def handle(self):
        global myCar
        global myLaser
        global myBuzzer
        global myRGBLighter
        global myDistanceChecker
        commandBuffer = ""
        commandEntered = False
        a = "r"
        exitCommandLoop = False
        while not exitCommandLoop:
            a = self.request.recv(1)

            if a:
                try:
                    if a != b'\r' and a != b'\n':
                        a = a.strip().decode("ascii")
                        print(a)
                except:
                    a = ""
                if a == b'\n':
                    commandEntered = True
                elif a == b'\r':
                    pass
                else:
                    commandBuffer += a
                    
                if commandEntered:
                    if commandBuffer == "FORWARD":
                        myCar.forward()
                        commandEntered = False
                    elif commandBuffer == "BACKWARD":
                        myCar.backward()
                        commandEntered = False
                    elif commandBuffer == "STOP":
                        myCar.stop()
                        commandEntered = False
                    elif commandBuffer == "KILL":
                        myCar.stop()
                        self.connection.close()
                        def kill_me_please(server):
                            server.shutdown()
                        _thread.start_new_thread(kill_me_please, (self.server,))
                        commandEntered = False
                        exitCommandLoop = True
                    else:
                        commandEntered = False
                    commandBuffer = ""
                else:
                    pass
            else:
                pass
                      
        
    # def log(self,message):
        # print(message)
                
    # def logTimed(self,message):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # print(current_time + " | " + message)
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
        
class ThreadedTCPRequestHandlerSample(BaseRequestHandler):
    # def setup(self):
        # print("[+] New server socket thread started for " + str(self.client_address[1]))

    def handle(self):
        self.data = self.rfile.readline().strip().decode()
        self.lastResult = sampleCommandProcessor.processCommand(self.data)
        self.wfile.write(self.lastResult.encode())
        self.rfile.flush()
        self.wfile.flush()
        
        if self.lastResult == "END":
            self.connection.close()
            def kill_me_please(server):
                server.shutdown()
            _thread.start_new_thread(kill_me_please, (self.server,))
        
    # def log(self,message):
        # print(message)
                
    # def logTimed(self,message):
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")
        # print(current_time + " | " + message)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    

def runTheServer(): 
    GPIO.setmode(GPIO.BCM)
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "192.168.0.108", 1700
    CarCommanderRequestHandler.DefineTheCar()
    CarCommanderRequestHandler.DefineTheLaser()
    CarCommanderRequestHandler.DefineTheBuzzer()
    CarCommanderRequestHandler.DefineTheRGBLighter()
    CarCommanderRequestHandler.DefineTheDistanceChecker()
    #server = TCPServer((HOST, PORT), ThreadedTCPRequestHandlerSample)
    server = None
    try:
        server = TCPServer((HOST, PORT), CarCommanderRequestHandler)
        socketserver.TCPServer.allow_reuse_address = True
        server.allow_reuse_address = True
        server.timeout = 5
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
    except Exception:
        if server:
            server.shutdown()
    GPIO.cleanup()
    if server:
        server.server_close()
    sys.exit(0)
if __name__ == "__main__":
    runTheServer()
