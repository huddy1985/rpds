#!/usr/bin/env python
import SocketServer
from time import ctime
import threading

HOST = '107.170.65.195'
PORT = 8001
ADDR = (HOST, PORT)
SOCKTIMEOUT = 10*60

def drivingSend(conn):
    while True:
        print 'cur request is {}'.format(conn)
        input = raw_input("what do you want to send:")
        print "send is " + input
        conn.sendall(input)

class MyRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(1800)
        try:
                print '...connected from:', self.client_address
                print '...self.request is {}'.format(self.request)
                while True:
                    self.data = self.request.recv(40)
                    print('recv ' + self.data)
                    t1 = threading.Thread(target=drivingSend, args=(self.request,))
                    t1.setDaemon(True)
                    t1.start()
                    self.request.sendall('recv ' + self.data)
        except socket.timeout as e:
            print '{} catch an timeout exception. {}({})'.format(time.time(), e, self.client_address)
            self.finish()


tcpServ = SocketServer.ThreadingTCPServer(ADDR, MyRequestHandler)
print 'waiting for connection...'
# tcpServ.serve_forever()
tcpServ.handle_request()
