import logging
from datetime import datetime
import sys
import traceback
from logging.handlers import TimedRotatingFileHandler, SysLogHandler

FORMATTER = logging.Formatter("%(asctime)s : LOGGER<%(name)s> : LEVEL<%(levelname)s> : MESSAGE %(message)s ")
LOG_FILE = "monday.log"

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    if exc_traceback:
        logging.critical(traceback.format_tb(exc_traceback))

def get_console_handler():
   console_handler = logging.StreamHandler(sys.stdout)
   console_handler.setLevel(logging.INFO)
   console_handler.setFormatter(FORMATTER)
   return console_handler

def get_file_handler():
   file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
   file_handler.setLevel(logging.DEBUG)
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_stream_hanlder():
    stream_handler = SysLogHandler(address=('logs6.papertrailapp.com', 11789))
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(FORMATTER)
    return stream_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG) # better to have too much log than not enough
    if not logger.handlers:
        logger.addHandler(get_console_handler())
        # logger.addHandler(get_file_handler())
        # logger.addHandler(get_stream_hanlder())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    # sys.excepthook = handle_exception
    # logger = logging.LoggerAdapter(logger, extra)
    return logger