import gprs.gprs as cgprs
import tools.tools as tools
import threading
import serial

g_gprs = cgprs.gprs()
g_sent = 0

def gprs():
    global g_sent
    config_json = tools.initJson()

    g_gprs.init('/dev/ttyUSB0', 115200, 8, 'N', 1, 1, 'DT')
    g_gprs.setWorkMode(0)
    test = g_gprs.test()
    print test

    if '0' == config_json['gprs_conf']['IMEI'] or config_json['gprs_conf']['IMEI'] == '':
        if g_gprs.imei != '':
            config_json['gprs_conf']['IMEI'] = str(g_gprs.imei)
        else:
            print 'json and gprs imei is nil'
            imei = g_gprs.getIMEI()
            config_json['gprs_conf']['IMEI'] = imei
            print 'get imei ' + imei
        tools.setValue2Json()

    # set register pkt content
    if '' == config_json['gprs_conf']['dtu']['pkt_register_content']['login_data']:
        print 'register content is nil'
        imei = config_json['gprs_conf']['IMEI']
        if not imei:
            imei = g_gprs.getIMEI()
            config_json['gprs_conf']['IMEI'] = imei
            tools.setValue2Json()
        login_data = tools.string2hex(str(imei) + '--logined: ')
        g_gprs.setPktRegisterContent(login_data, 0)
        config_json['gprs_conf']['dtu']['pkt_register_content']['login_data'] = login_data
        tools.setValue2Json()

    # set heartbeat content
    if '' == config_json['gprs_conf']['dtu']['pkt_heartbeat_content']['heartbeat_data']:
        imei = config_json['gprs_conf']['IMEI']
        if not imei:
            imei = g_gprs.getIMEI()
            config_json['gprs_conf']['IMEI'] = imei
            tools.setValue2Json()
        heart_data = tools.string2hex(str(imei) + '--heartbeat:')
        g_gprs.setHeartBeatContent(heart_data, 0)
        config_json['gprs_conf']['dtu']['pkt_heartbeat_content']['heartbeat_data'] = heart_data
        tools.setValue2Json()

    while True:
        ret = g_gprs.getNetStatus()
        print 'ret :' + ret
        if ':' in ret:
            netstatus = ret.split(':')[1]
            print netstatus
            if netstatus.split(',')[0] == '0':
                print 'no connect to server'
                g_gprs.conn2('TCP', '107.170.65.195', '8002')
                g_gprs.msleep(10000)
            else:
                print 'already connect to server'
                g_gprs.ser.flushOutput()
                g_gprs.ser.flushInput()
                break

    # return to the pre mode working
    g_gprs.setEntm()

    id = 0
    while True:
        data = raw_input("what you want to send: ")
        if data:
            imei = g_gprs.imei
            if imei.strip() == '':
                imei = config_json['gprs_conf']['IMEI']

            g_gprs.sendData(str(int(imei) + int(id)) + ':' + data)
            g_sent = 1
        id += 1

def recvmsg():
    print 'recv msg thread'
    global g_sent
    while True:
        g_gprs.msleep(1000)
        try:
            output = g_gprs.recv()
            if len(output) > 0:
                print output
        except serial.serialutil.SerialException:
            continue

threads = []
if __name__ == "__main__":
    t1 = threading.Thread(target=recvmsg, args='')
    threads.append(t1)
    for t in threads:
        t.setDaemon(True)
        t.start()
    gprs()




