import logging
import os
import config
from server import server
from logging.handlers import SysLogHandler
from logging.handlers import TimedRotatingFileHandler

level = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARN,
    "error": logging.ERROR
}




