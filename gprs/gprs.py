# encoding=utf-8
import serial
import time
import sys
sys.path.append('..')
from mlog.log import rpdt_logging


PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)
GPRS_MODE_DATA_TRANSPARENT, GPRS_MODE_MSG_TRANSPARENT, GPRS_MODE_HTTP_TRANSPARENT, GPRS_MODE_AT = 'DT', 'MT', 'HTTP', 'AT'

GPRS_MOD = {
    "0" : "data transparent",
    "1" : "serial cmd",
    "2" : "AT command",
    "3" : "HTTP client",
    "4" : "msg mode"
}

class gprs:
    def __init__(self):
        self.g_status = ['entm', 'ok']
        self.g_c_status = str()
        self.ser = serial.Serial()
        self.port = str()
        self.selBaudRate = int()
        self.bytesize = int()
        self.selParity = PARITY_NONE
        self.stopbits = STOPBITS_ONE
        self.timeout = 1
        self.log = rpdt_logging()
        self.log.init(20)
        self.mode = GPRS_MODE_DATA_TRANSPARENT
        self.imei = -1

    def msleep(self, timeout):
        time.sleep(timeout/1000)

    def init(self, port, selBaudRate, bytesize, selParity, stopbits, timeout, mode = GPRS_MODE_DATA_TRANSPARENT):
        self.selBaudRate = selBaudRate
        self.bytesize = bytesize
        self.selParity = selParity
        self.stopbits = stopbits
        self.timeout = timeout
        self.port = port
        self.mode = mode

        self.open()
        self.g_c_status = self.g_status[0]
        self.setWorkMode(0)
        self.imei = self.getIMEI().replace('OK', '')

        curmod = self.getWorkMode()
        if curmod != -1 and curmod in (0, 1, 2, 3, 4):
            print 'cur mode is ' + GPRS_MOD[str(curmod)]
            self.setWorkMode(0)

        while self.g_c_status != self.g_status[1]:
            tryplus = 10
            while tryplus >= 0 and self.g_c_status != self.g_status[1]:
                self.msleep(250)
                self.send('+++')
                output = self.recv()
                tryplus -= 1
                if 'a' in output:
                    trya = 10
                    while trya >= 0 and self.g_c_status != self.g_status[1]:
                        self.send('a')
                        ok = self.recv()
                        if '+ok' in ok:
                            self.g_c_status = self.g_status[1]
                            self.log.info("enter temp instruction mode, current status is " + self.g_c_status)
                            print "enter temp instruction mode, current status is " + self.g_c_status
                            break
                            trya -= 1
                else:
                    self.setEntm()
            self.msleep(250)

    @property
    def mode(self):
        return self.mode

    @mode.setter
    def mode(self, mode):
        self.mode = mode

    @property
    def imei(self):
        return self.imei

    def reset(self):
        pass

    def open(self):
        # selComPort = '/dev/ttyUSB0'

        self.ser = serial.Serial(port=self.port
                            , baudrate=self.selBaudRate
                            , bytesize=self.bytesize
                            , parity=self.selParity
                            , stopbits=self.stopbits
                            , timeout=self.timeout)
        if self.ser.isOpen():
            self.log.info("open serial suc")
        else:
            self.log.info("open serial fail")
            exit

    def send(self, cmd, timeout = 0):
        self.log.info(cmd)
        print cmd
        self.ser.write(cmd + '\r')
        if (timeout > 0):
            self.msleep(timeout)

    def recv(self):
        output = ''
        try:
            output = self.ser.readall().strip().replace('\r', '').replace('\n', '')
            # print output
            return output
        except serial.serialutil.SerialException, e:
            print e.message
            return output

    def getSerialINfo(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+ICF?')
        output = self.recv()
        self.log.info(output)


    # very inportant
    # 功能:查询 DTU 当前参数,除串口参数外的所有参数均由此指令查询。
    # 返回示例:
    # +CIPCFG: 1, 30, 0, 100, 10, 1800
    # (心跳时间:30s,打包时间:100ms,打包长度:10,自动重启时间:1800s)
    # +CIPPACK: 0, "31313131",1
    # (心跳包数据:“1111”,向串口发送)
    # +CIPPACK: 1, "31303031" , 0
    # (注册包数据:“1001”,最后一个参数为 0 表示连接即发注册包,如果为 1 表示数据带注册包)
    # +CSTT: "uninet", "", ""
    # (APN 信息,分别为 APN 账号、用户名、密码)
    # +CIPNUM: 10086
    # (短信透传模式下目的号码为 10086)
    # +CIPSTART:1,"TCP", "usrcn.gicp.net",10101, 1
    # (网络连接信息,表示第 1 路连接,TCP 协议,目标地址:usrcn.gicp.net,启用)
    # +CIPSTART:2,"TCP", "usrcn.gicp.net",10102, 1
    # (网络连接信息,表示第 2 路连接,TCP 协议,目标地址:usrcn.gicp.net,启用)
    # +CIPSTART:3,"TCP", "usrcn.gicp.net",10103, 0
    # (网络连接信息,表示第 3 路连接,TCP 协议,目标地址:usrcn.gicp.net,未启用)
    # +CIPSTART:4,"TCP", "usrcn.gicp.net",10104, 1
    # (网络连接信息,表示第 4 路连接,TCP 协议,目标地址:usrcn.gicp.net,启用)
    # +CIMOD: 2
    # (工作模式,0 为透传模式、1 为串口命令模式,2 为 AT 指令模式,3 为 HTTPD Client 模式,4
    # 为短信透传模式)
    # +CINETAT:0
    # (透传模式下网络 AT 命令使能:0 为不使能网络 AT 命令,1 为使能网络 AT 命令)
    # +CICOMAT:0
    # (透传模式下串口 AT 命令使能:0 为不使能串口 AT 命令,1 为使能串口 AT 命令)
    # +CINETPT:1,0
    # (第一路连接本地端口)
    # +CINETPT:2,0
    # (第二路连接本地端口)
    # +CINETPT:3,0
    # (第三路连接本地端口)
    # +CINETPT:4,0
    # (第四路连接本地端口)
    # OK
    def getDTU(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CIPSCONT?')
        output = self.recv()
        self.log.info(output)
        return output

    def getBasement(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CILAC?')
        output = self.recv()
        self.log.info(output)

    def getIP(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CIDTUIP?')
        output = self.recv()
        self.log.info(output)

    def test(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT')
        output = self.recv()
        self.log.info(output)
        return output

    def getIMEI(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CGSN')
        output = self.recv().replace('OK', '')
        self.log.info(output)
        return output

    def getCurTime(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CCLK?')
        output = self.recv()
        self.log.info(output)

    def getSignalStrength(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CSQ')
        output = self.recv()
        self.log.info(output)

    def getNetRegInfo(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+COPS?')
        output = self.recv()
        self.log.info(output)

    def getSIMSMS(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CMGL=4')
        output = self.recv()
        self.log.info(output)

    def getSimNum(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CSCA?')
        output = self.recv()
        self.log.info(output)

    # MOD 表示工作模式,为 0 表示透传模式,为 1 表示串口命令模式,为 2 表示 AT 指令模式,为 3
    # 表示为 HTTPD Client 模式,为 4 表示短信透传模式
    def setWorkMode(self, mode):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CIMOD="' + str(mode) + '"')
        output = self.recv()
        self.log.info(output)

    def getWorkMode(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        output = self.getDTU()
        # print output
        if '+CIMOD:' in output:
            pos_start = output.find('+CIMOD:')
            pos_end = output.find('+CINETAT:1')
            # many line end '2\r\n\r'
            mod = output[pos_start + 8:pos_end - 4]
            self.log.info('mod is ' + mod)
            return mod
        return -1

    # AT+CIPSCONT=PNUM, "PORTOCOL","ADDRESS", "PORT",START
    # PNUM     表示配置第 PNUM     个连接。
    # PORTOCOL     表示连接的协议是    UDP / TCP。
    # ADDRESS    表示目的地址。
    # PORT    表示目标端口。
    # START    表示是否启用, 0    为不启用, 1    为启用。
    # 返回: OK
    # 示例:AT + CIPSCONT = 1, "TCP", "usrcn.gicp.net", 10101, 1 < CR >
    def setConnection(self, whichone, protocol, address, port, enable):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CIPSCONT={0},"{1}","{2}",{3},{4}'.format(whichone, protocol, address, port, enable))
        output = self.recv()
        self.log.info(output)

    def setEntm(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+ENTM')
        output = self.recv()
        self.log.info(output)

    # AT + CINETAT = 0 < CR >
    # 功能:禁用网络
    # AT
    # 指令功能。
    # AT + CINETAT = 1 < CR >
    # 功能:启用网络
    # AT
    # 指令功能。
    def setNetAT(self, enable):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CINETAT=' + str(enable))
        output = self.recv()
        self.log.info(output)

    # 设置透传模式下模块联网方式为短连接/长连接。为 0 则设置为短连接,为 1 则设置为长连接。
    def setNetMode(self, mode):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CISOCLINK=' + str(mode))
        output = self.recv()
        self.log.info(output)

    def getNetStatus(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CINET?')
        output = self.recv()
        self.log.info(output)
        return output

    # AT + CIOPEN = PORTOCOL, ADDRESS, PORT < CR >
    # 功能:用于在 AT 指令模式下发起网络连接
    # 参数解析:
    # PORTOCOL    表示发起连接的协议类型, 取值“TCP”或者“UDP”。
    # ADDRESS     表示目的地址, 可以是
    # IP          地址或者域名。
    # PORT        表示目的端口号。
    # 示例:
    # 发送:AT + CIOPEN = TCP, usrcn.gicp.net, 10101 < CR > < LF > 发送发起连接指令
    # 返回:OK                指令执行 OK
    # 返回:CONNECT OK        网络连接建立 OK
    def conn2(self, protocol, address, port):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CIOPEN=' + protocol + ',' + address + ',' + port)
        output = self.recv()
        self.log.info(output)

    # AT + CISEND < CR >
    # 功能:用于在     AT     指令模式下, 建立网络连接以后向网络发送数据。
    # 示例:
    # 发送:AT + CISEND < CR > < LF >
    # 返回: >
    # 发送:test
    # 返回:SEND     OK
    def sendData(self, data):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        if len(data) == 0:
            return
        print 'send data:' + data
        self.ser.write(data)
        self.log.info('send data:' + data)

    def recvData(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        output = self.recv()
        print output
        return output

    def closeConn(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CICLOSE')
        output = self.recv()
        self.log.info(output)

    # AT + CIPCFG = 1, HEAT, 0, TIME, LEN, RTIME < CR >
    # 参数解析:
    # HEAT    表示心跳包发送时间间隔, 单位秒。当设定的时间内没有网络数据传输, 模块将会向服务器发送心跳包维持连接, 设置时间为
    #         0秒时心跳功能禁用。
    # TIME    表示串口打包时间, 单位毫秒。设定时间内串口没有接收到新的数据则将已接收到的数据
    #         打包。
    # LEN     表示打包长度, 暂未启用。
    # RTIME   表示自动重启时间, 单位秒。当设定的时间内没有串口数据同时没有网络数据接收, 则模
    #         块重启, 当设定的时间小于600秒时, 自动重启功能禁用。
    # 返回: OK
    # 示例:AT + CIPCFG = 1, 30, 0, 100, 10, 1800 < CR >。
    # 说明:配置心跳时间    30s, 串口打包时间100ms, 打包长度10, 自动重启时间1800s。
    def setHeartBeat(self, heat, time, len, rsTime):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        data = 'AT+CIPCFG=1,{0},0,{1},{2},{3}'.format(heat, time, len, rsTime)
        self.send(data)
        output = self.recv()
        self.log.info(output)


    # AT + CIPPACK = 0, "HEATDATA", "STA" < CR >
    # 参数解析:     HEATDATA     表示心跳包数据内容, 十六进制表示, 每两个字节表示一个十六进制数。心跳包最大长度为40字节。
    # STA          表示心跳数据发送方向, 0为心跳包向网络发送, 1表示心跳数据向串口发送。
    # 返回: OK
    # 示例:AT + CIPPACK = 0, "31313131", "1" < CR >。
    # 说明:配置心跳包为数字    1111(数字1的 ASCII 码值为 0x31), 心跳数据向串口发送。
    def setHeartBeatContent(self, data, dir):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        data = 'AT+CIPPACK=0,"{0}","{1}"'.format(data,dir)
        self.send(data)
        output = self.recv()
        self.log.info(output)

    # LOGINDATA    表示注册包数据, 格式同心跳包。
    # STATUS       表示注册包启用方式, 0 为连接即发注册包, 1 为发送数据带注册包。注册包最大长度为40字节。
    # 返回: OK
    # 示例:AT + CIPPACK = 1, "31303031", "0" < CR >。
    # 说明:注册包为数字    1001, 连接即发注册包模式。
    def setPktRegisterContent(self, data, status):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        data = 'AT+CIPPACK=1,"{0}","{1}"'.format(data, status)
        self.send(data)
        output = self.recv()
        self.log.info(output)
