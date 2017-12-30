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

class analog_io():
    def __init__(self):
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

    def open(self, port, selBaudRate, bytesize, selParity, stopbits, timeout):
        # selComPort = '/dev/ttyUSB1'
        self.selBaudRate = selBaudRate
        self.bytesize = bytesize
        self.selParity = selParity
        self.stopbits = stopbits
        self.timeout = timeout
        self.port = port

        self.ser = serial.Serial(port=self.port
                                 , baudrate=self.selBaudRate
                                 , bytesize=self.bytesize
                                 , parity=self.selParity
                                 , stopbits=self.stopbits
                                 , timeout=self.timeout)
        if self.ser.isOpen():
            self.log.info("open serial suc")
            print 'open serial suc'
        else:
            self.log.info("open serial fail")
            print 'open serial fail'
            exit

    def send(self, data):
        self.log.info(data)
        print data
        self.ser.write(data + '\r')

    def recv(self):
        output = ''
        try:
            output = self.ser.readall().strip().replace('\r', '').replace('\n', '')
            print output
            return output
        except serial.serialutil.SerialException, e:
            print e.message
            return output