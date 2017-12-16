# encoding=utf-8

import serial
import time
from log import rpdt_logging
import sys

PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'
STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO = (1, 1.5, 2)
FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS = (5, 6, 7, 8)

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

    def msleep(self, timeout):
        time.sleep(timeout/1000)

    def init(self, port, selBaudRate, bytesize, selParity, stopbits, timeout):
        self.selBaudRate = selBaudRate
        self.bytesize = bytesize
        self.selParity = selParity
        self.stopbits = stopbits
        self.timeout = timeout
        self.port = port

        self.open()
        self.g_c_status = str()
        while self.g_c_status != self.g_status[0]:
            self.send('AT+ENTM')
            output = self.recv()
            if 'OK' in output:
                self.g_c_status = self.g_status[0]
                self.log.info("current status is " + self.g_c_status)
                break

        while self.g_c_status != self.g_status[1]:
            tryplus = 10
            while tryplus >= 0 and self.g_c_status != self.g_status[1]:
                self.send('+++')
                output = self.recv()
                self.msleep(300)
                tryplus -= 1
                if 'a' in output:
                    # print "get output a"
                    trya = 10
                    while trya >= 0 and self.g_c_status != self.g_status[1]:
                        self.send('a')
                        ok = self.recv()
                        if '+ok' in ok:
                            self.g_c_status = self.g_status[1]
                            self.log.info("enter temp instruction mode, current status is " + self.g_c_status)
                            break
                            trya -= 1
            self.msleep(250)

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
        self.ser.write(cmd + '\r')
        if (timeout > 0):
            self.msleep(timeout)

    def recv(self):
        output = self.ser.readall()
        self.log.info(output)
        return output

    def getSerialINfo(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+ICF?')
        output = self.recv()


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

    def getBasement(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CILAC?')
        output = self.recv()

    def getIP(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CIDTUIP?')
        output = self.recv()

    def test(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT')
        output = self.recv()

    def getIMEI(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CGSN')
        output = self.recv()

    def getCurTime(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CCLK?')
        output = self.recv()

    def getSignalStrength(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+CSQ')
        output = self.recv()

    def getNetRegInfo(self):
        self.log.debug(sys._getframe().f_code.co_filename)
        self.log.debug(sys._getframe().f_code.co_name)
        self.log.debug(sys._getframe().f_lineno)
        self.send('AT+COPS?')
        output = self.recv()




