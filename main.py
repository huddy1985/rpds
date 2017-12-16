import gprs

if __name__ == "__main__":
    gprs = gprs.gprs()
    gprs.init('/dev/ttyUSB0', 115200, 8, 'N', 1, 1)
    gprs.test()

    gprs.getSignalStrength()