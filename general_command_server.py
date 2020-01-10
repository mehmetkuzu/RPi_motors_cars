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
    def __init__(self, commanderFunctions, serverHost, serverPort):
        self.commanderFunctions = commanderFunctions
        self.serverHost = serverHost
        self.serverPort = serverPort

    def runTheServer(self): 
        # Port 0 means to select an arbitrary unused port
        HOST, PORT = self.serverHost, self.serverPort
        server = None
        try:
            server = ThreadingTCPServer((HOST, PORT), CommanderRequestHandler)
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
    host = "0.0.0.0"
    port = 1700

    testServer = GeneralCommandServer(GenericCommanderFunctionsClass(), host, port)
    testServer.runTheServer()
    sys.exit(0)
    runTheServer()
