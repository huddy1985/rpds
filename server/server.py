#!/usr/bin/env python
import SocketServer
from time import ctime
import threading

HOST = '107.170.65.195'
PORT = 8001
ADDR = (HOST, PORT)


def drivingSend(conn):
    while True:
        input = raw_input("what do you want to send:")
        print "send is " + input
        conn.sendall(input)


class MyRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print '...connected from:', self.client_address
        while True:
            self.data = self.request.recv(40)
            print('recv ' + self.data)
            t1 = threading.Thread(target=drivingSend, args=(self.request,))
            t1.setDaemon(True)
            t1.start()


tcpServ = SocketServer.ThreadingTCPServer(ADDR, MyRequestHandler)
print 'waiting for connection...'
tcpServ.serve_forever()
