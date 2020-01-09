#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  general_command_server.py
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
import sys
from socketserver import ThreadingTCPServer
from commander_request_handler import CommanderRequestHandler
from commander_request_handler import GenericCommanderFunctionsClass
class GeneralCommandServer:
    def __init__(self, commanderFunctions):
        self.commanderFunctions = commanderFunctions

    def runTheServer(self): 
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = "172.16.40.1", 1700
        #server = TCPServer((HOST, PORT), ThreadedTCPRequestHandlerSample)
        server = None
        try:
            server = ThreadingTCPServer((HOST, PORT), CommanderRequestHandler)
            #socketserver.TCPServer.allow_reuse_address = True
            server.allow_reuse_address = True
            server.timeout = 5
            server.commanderFunctions = self.commanderFunctions
            server.doTheShutting = False
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        # except Exception:
            # if server:
                # server.shutdown()
        if server:
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    testServer = GeneralCommandServer(GenericCommanderFunctionsClass())
    testServer.runTheServer()
    sys.exit(0)
    runTheServer()
