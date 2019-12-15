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
        a = "r"
        while a != "q" and a!= "k":
            a = self.request.recv(1)
            print(a)
            if a:
                try:
                    a = a.strip().decode("ascii")
                except:
                    a = " "
                    
                if a == "f":
                    myCar.forward()
                elif a == "b":
                    myCar.backward()
                elif a == "r":
                    myCar.turnRight()
                elif a == "l":
                    myCar.turnLeft()
                elif a == "+":
                    myCar.gearUp(1)
                elif a== "-":
                    myCar.gearDown(1)
                elif a == "s":
                    myCar.stop()
                elif a == "t":
                    myLaser.turnOff()
                elif a == "T":
                    myLaser.turnOn()
                elif a == "/":
                    myBuzzer.turnOff()
                elif a == "*":
                    myBuzzer.turnOn()
                elif a == ".":
                    myRGBLighter.doTheShowOnThread()                
                else:
                  pass
            else:
                pass
                      


        if a=="k":
            myCar.stop()
            GPIO.cleanup()

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
    HOST, PORT = "192.168.0.105", 1700
    CarCommanderRequestHandler.DefineTheCar()
    CarCommanderRequestHandler.DefineTheLaser()
    CarCommanderRequestHandler.DefineTheBuzzer()
    CarCommanderRequestHandler.DefineTheRGBLighter()
    #server = TCPServer((HOST, PORT), ThreadedTCPRequestHandlerSample)
    server = TCPServer((HOST, PORT), CarCommanderRequestHandler)
    try:
        server.allow_reuse_address = True
        server.timeout = 20
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
    server.server_close()
    sys.exit(0)
if __name__ == "__main__":
    runTheServer()
