import gprs.gprs as gprs

if __name__ == "__main__":
    gprs = gprs.gprs()
    gprs.init('/dev/ttyUSB0', 115200, 8, 'N', 1, 1)
    gprs.test()
    # gprs.getIP()
    gprs.msleep(300)
    # gprs.getDTU()
    gprs.setNetMode(1)
    gprs.msleep(300)
    # gprs.setNetAT(1)
    # gprs.msleep(300)
    # gprs.getDTU()
    # gprs.msleep(300)
    # gprs.setConnection(1, 'TCP', '107.170.65.195', 8001, 1)
    # gprs.msleep(300)
    # gprs.getDTU()
    # gprs.conn2('TCP', '107.170.65.195', '8001')
    gprs.msleep(200)
    # gprs.getNetStatus()
    # gprs.msleep(200)
    gprs.sendData('test')
    gprs.msleep(10000)
    # gprs.closeConn()




