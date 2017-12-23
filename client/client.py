import socket
HOST = '107.170.65.195'
PORT = 8001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = raw_input("Please input msg:")
    if 'quit' in cmd:
        break
    s.send(cmd)
    data = s.recv(1024)
    print data
s.close()
