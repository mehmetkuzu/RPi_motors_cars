#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  commander_request_handlerx.py
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
import threading
import _thread
from socketserver import StreamRequestHandler
import socket

class CommandReturns:
    def __init__(self, statusOK, statusEND, returnMessage):
        self.statusOK = statusOK
        self.statusEND = statusEND
        self.returnMessage = returnMessage

class GenericCommanderFunctionsClass:
        
    def processCommand(self, commandString):
        if commandString == "KILL":
            return CommandReturns(True,True, "Shutting down server")
        elif commandString == "HALO":
            return CommandReturns(True,False, "Halo dayı halo")
        elif commandString == "PING":            
            return CommandReturns(True,False, "Pong")
        else:
            print (commandString)
            return CommandReturns(False,False, "Invalid Command, boomer")

class CommanderRequestHandler(StreamRequestHandler):
    def handle(self):       
        print("CONNECTION: " + self.connection.getpeername()[0])
        self.connection.settimeout(5)
        commandBuffer = ""
        commandEntered = False
        a = "r"
        exitCommandLoop = False
        while not exitCommandLoop:
            if self.connection._closed:
                print("Connection closed")
            if self.server.doTheShutting:
                print ("someone closed the server")
                self.connection.close()
                break
            try:
                a = self.request.recv(1)
            except socket.timeout:
                continue

            if a:
                print(a)
                try:
                    if a != b'\r' and a != b'\n':
                        a = a.decode("ascii")
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
                    print(commandBuffer)
                    returning = self.server.commanderFunctions.processCommand(commandBuffer)
                    retMessage = (returning.returnMessage + "\n").encode('utf-8')
                    if returning.statusEND:
                        self.request.sendall(retMessage)
                        self.connection.close()
                        def kill_me_please(server):
                            server.doTheShutting = True
                            server.shutdown()
                        _thread.start_new_thread(kill_me_please, (self.server,))
                        commandEntered = False
                        exitCommandLoop = True
                    elif returning.statusOK:
                        self.request.sendall(retMessage)
                        commandBuffer = ""
                        commandEntered = False
                    else:
                        self.request.sendall(retMessage)
                        commandBuffer = ""
                        commandEntered = False

                pass
