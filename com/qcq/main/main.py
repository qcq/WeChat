#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import os
import logging
import logging.handlers
import signal
import sys
import traceback
import datetime
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from wsgilog import WsgiLog
import argparse

from com.qcq.handles.url_mapping import app
import com.qcq.access_token as access_token
import com.qcq.media.media as media
import com.qcq.handles.baidu as baidu
from com.qcq.monitoring.picture_path_handler import PicturePathHandler
from com.qcq.const import system_info

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(filename)s-%(funcName)s:%(lineno)d:%(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FILE_NAME = r'/home/chuanqin/WeChat/com/qcq/main/static/single_log.log'
WEB_LOG_FILE_NAME = r'/home/chuanqin/WeChat/com/qcq/main/static/web_log.log'
ROTATE_LOG_FILE_NAME = r'/home/chuanqin/WeChat/com/qcq/main/static/rotate_log.log'


def shutdown(signum, frame):
    system_info.time_end = datetime.datetime.now()
    system_info.running_time = system_info.time_end - system_info.time_start
    logging.info("the system stopped at %s, runninged %s."
                 % (system_info.time_end.ctime(), system_info.running_time))
    logging.info('The system is going down by the ctrl+c signal. %s/%s'
        % (signum, frame))
    sys.exit()


class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat=LOG_FORMAT,
            tofile=True,
            toprint=True,
            file=WEB_LOG_FILE_NAME,
            interval='d',
            backups='3'
        )

def __setLogger__():
    logFormatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    fileHandler = logging.FileHandler(LOG_FILE_NAME)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    rotateHandler = logging.handlers.RotatingFileHandler(ROTATE_LOG_FILE_NAME, mode="w",
        maxBytes=1000000, backupCount=100, encoding='utf-8')
    rotateHandler.setFormatter(logFormatter)
    rootLogger.addHandler(rotateHandler)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    # here consider add the email handler to report the error in time.


def __parser_command_line__():
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=int, help='input the http port of web.py', default=80)
    parser.add_argument("-d", "--deletelog", help="delete the previous log", action="store_true", default=True)
    args = parser.parse_args()
    if args.deletelog:
        os.remove(LOG_FILE_NAME)
        os.remove(WEB_LOG_FILE_NAME)
        os.remove(ROTATE_LOG_FILE_NAME)

if __name__ == '__main__':
    system_info.time_start = datetime.datetime.now()
    __parser_command_line__()
    __setLogger__()
    logging.info("the system started at %s" % system_info.time_start.ctime())
    token = access_token.Token()
    uploadPicture = media.Media()
    netDisk = baidu.BaiDu()
    # below code to take pyeventbus work
    uploadPicture.register(uploadPicture)
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
        netDisk.setDaemon(True)
        netDisk.start()
        logging.info("server is running to providing service to baidu netdisk.")
        pictureMonitor = PicturePathHandler(patterns=[r'*.jpg', r'*.png', r'*.jpeg', r'*.gif', r'*.JPG', r'*.PNG', r'*.JPEG', r'*.GIF'],
            ignore_patterns=[r'*.swap'], ignore_directories=True, case_sensitive=True)
        # below code to take pyeventbus work
        pictureMonitor.register(pictureMonitor)
        watch = observer.schedule(pictureMonitor, path='..//pictures', recursive=True)
        observer.add_handler_for_watch(LoggingEventHandler(), watch)
        observer.start()
        logging.info("start to monitor the path of picture.")
        logging.info("server is ready to provide the service.")

        app.run(Log)
    except KeyboardInterrupt:
        observer.stop()
    except Exception, exc:
        logging.warn('Exception happened:%s' %
            traceback.print_exc(), exc_info = True)
