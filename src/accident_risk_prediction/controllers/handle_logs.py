# pylint: disable=too-few-public-methods
""" Define logging system """

import sys
import logging
from logging.handlers import SysLogHandler
import time


class NoErrorFilter(logging.Filter):
    """ Excludes all logs levels errors """

    def filter(self, record):
        return record.levelno != logging.ERROR


def get_formatter():
    """" Return the format of the log message """
    return "%(name)-4s %(asctime)-6s %(levelname)-8s %(message)s"


def get_datefmt():
    """ Return date formatter """
    return "%m-%d-%Y %H:%M:%S"


def apply_syslog_config():
    """ apply Handle Syslog """
    syslog_handler = SysLogHandler(
        address='/dev/log')
    syslog_handler.setFormatter(logging.Formatter(
        get_formatter(), get_datefmt()))
    return syslog_handler


def apply_console_handler():
    """ apply Console Handler """
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.addFilter(NoErrorFilter())
    return console_handler


def apply_error_stream_handler():
    """ Apply Stream Handler to send logging.ERROR to stderr """
    error_handler = logging.StreamHandler(stream=sys.stderr)
    error_handler.setLevel(level=logging.ERROR)
    return error_handler


def conf_logging():
    """ apply basic config log """
    logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                        level=logging.DEBUG,
                        datefmt=get_datefmt(),
                        handlers=[apply_console_handler(),
                                  apply_syslog_config(),
                                  apply_error_stream_handler()])
    logging.Formatter.converter = time.gmtime
