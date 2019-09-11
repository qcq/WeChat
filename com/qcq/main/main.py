#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import logging
import logging.handlers
import signal
import sys
import traceback
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

from com.qcq.handles.url_mapping import app
import com.qcq.access_token as access_token
import com.qcq.media.media as media
from com.qcq.monitoring.picture_path_handler import PicturePathHandler

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(filename)s-%(funcName)s:%(lineno)d:%(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FILE_NAME = r'/home/chuanqin/logs/single_log.log'
ROTATE_LOG_FILE_NAME = r'/home/chuanqin/logs/rotate_log.log'


def shutdown(signum, frame):
    logging.info('The system is going down by the ctrl+c signal. %s/%s'
        % (signum, frame))
    sys.exit()


def __setLogger():
    logFormatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(LOG_FILE_NAME)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    rotateHandler = logging.handlers.RotatingFileHandler(ROTATE_LOG_FILE_NAME, mode="w",
        maxBytes=10000, backupCount=3)
    rotateHandler.setFormatter(logFormatter)
    rootLogger.addHandler(rotateHandler)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


if __name__ == '__main__':
    __setLogger()
    token = access_token.Token()
    uploadPicture = media.Media()
    observer = Observer()
    try:
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)
        token.setDaemon(True)
        token.start()
        logging.info("server is get access token thread is running in Daemon mode.")
        uploadPicture.setDaemon(True)
        uploadPicture.start()
        logging.info("server is running to upload pictures to tencent.")
        pictureMonitor = PicturePathHandler(patterns=[r'*.jpg', r'*.png', r'*.JPG', r'*.PNG'],
            ignore_patterns=[r'*.swap'], ignore_directories=True, case_sensitive=True)
        watch = observer.schedule(pictureMonitor, path='..//pictures', recursive=True)
        observer.add_handler_for_watch(LoggingEventHandler(), watch)
        observer.start()
        logging.info("start to monitor the path of picture.")
        logging.info("server is ready to provide the service.")

        app.run()
    except KeyboardInterrupt:
        observer.stop()
    except Exception, exc:
        logging.warn('Exception happened:%s' %
            traceback.print_exc(), exc_info = True)
