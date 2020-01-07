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

class CommandReturns:
    def __init__(self, statusOK, statusEND, returnMessage):
        self.statusOK = statusOK
        self.statusEND = statusEND
        self.returnMessage = returnMessage

class GenericCommanderFunctionsClass:
        
    def processCommand(self, commandString):
        if commandString == "KILL":
            return CommandReturns(True,True, "Shutting down server")
        elif commandString != "HALO":
            return CommandReturns(False,False, "INVALID COMMAND Boomer")
        else:
            print (commandString)
            return CommandReturns(True,False, "OK Boomer")

class CommanderRequestHandler(StreamRequestHandler):
    def handle(self):        
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
                    returning = self.server.commanderFunctions.processCommand(commandBuffer)
                    retMessage = (returning.returnMessage + "\n").encode('utf-8')
                    if returning.statusEND:
                        self.request.sendall(retMessage)
                        self.connection.close()
                        def kill_me_please(server):
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
