#myLog.py
import logging
import getpass
import time

class CALog(object):
#class CALog(logging.Logger):
# Reference - 
# http://yhhuang1966.blogspot.com/2018/04/python-logging_24.html
    def __init__(self):
        user=getpass.getuser()
        self.logger=logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        format='%(asctime)s-%(levelname)s: %(message)s'
        formatter=logging.Formatter(format, datefmt='%Y%m%d-%H%M%S')
        streamhandler=logging.StreamHandler()
        streamhandler.setFormatter(formatter)
        self.logger.addHandler(streamhandler)
        logfile='./CA logs/' + user + time.strftime("-%Y-%b") + '.log'
        filehandler=logging.FileHandler(logfile, encoding="utf-8")
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)
    def debug(self, msg):
        self.logger.debug(msg)
    def info(self, msg):
        self.logger.info(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)
    def critical(self, msg):
        self.logger.critical(msg)
    def log(self, level, msg):
        self.logger.log(level, msg)
    def setLevel(self, level):
        self.logger.setLevel(level)
    def disable(self):
        logging.disable(50)