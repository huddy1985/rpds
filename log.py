import logging
import time
from time import gmtime, strftime

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

class rpdt_logging:
    def __init__(self):
        self.logging = logging
        self.filename = 'rpdt-' + strftime("%d-%b-%Y-%H:%M:%S", gmtime()) + '.log'
        self.level = DEBUG

    def init(self, level):
        self.level = level
        self.logging.basicConfig(filename=self.filename, format='%(levelname)s:%(message)s', level=self.level)

    def debug(self, output):
        self.logging.debug(output)

    def info(self, output):
        self.logging.info(output)

    def error(self, output):
        self.logging.error(output)
