import gprs.gprs as cgprs
import tools.tools as tools
import threading
import serial

g_gprs = cgprs.gprs()
g_sent = 0
def gprs():
    global g_sent
    g_gprs.init('/dev/ttyUSB0', 115200, 8, 'N', 1, 1, 'DT')
    g_gprs.test()
    g_gprs.msleep(300)
    while True:
        ret = g_gprs.getNetStatus()
        print ret
        netstatus = ret.split(':')[1]
        print netstatus
        if netstatus.split(',')[0] == '0':
            print 'no connect to server'
            g_gprs.conn2('TCP', '114.215.118.118', '8001')
            g_gprs.msleep(10000)
        else:
            print 'already connect to server'
            break

    id = 0
    #while True:
    data = raw_input("what you want to send: ")
    if data:
        g_gprs.sendData(str(id) + ':' + data)
        g_gprs.setEntm()
        g_sent = 1
    while True:
        print 'waiting msg'
        g_gprs.msleep(10000)

def recvmsg():
    print 'recv msg thread'
    global g_sent
    while True:
        if g_sent == 1:
            print 'start to read'
            g_gprs.msleep(1000)
            try:
                g_gprs.sendData('')
                output = g_gprs.recv()
                if len(output) > 0:
                    print output
            except serial.serialutil.SerialException, e:
                continue
            g_sent = 0
        g_gprs.msleep(1000)

threads = []
if __name__ == "__main__":
    t1 = threading.Thread(target=recvmsg, args='')
    threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    gprs()




