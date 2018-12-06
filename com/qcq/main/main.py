#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import logging
import signal
import sys
import traceback

from com.qcq.handles.url_mapping import app
import com.qcq.access_token as access_token
import com.qcq.media.media as media

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(filename)s-%(funcName)s:%(lineno)d:%(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FILE_NAME = r'/home/chuanqin/log.txt'


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
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


if __name__ == '__main__':
    __setLogger()
    try:
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)
        t = access_token.Token()
        t.setDaemon(True)
        t.start()
        logging.info(
            "server's get access token thread is running in Daemon mode.")
        uploadPicture = media.Media()
        uploadPicture.setDaemon(True)
        uploadPicture.start()
        logging.info("server is running to upload pictures to tencent.")
        logging.info("server is ready to provide the service.")

        app.run()
    except Exception, exc:
        logging.warn('Exception happened:%s' %
            traceback.print_exc(), exc_info = True, stack_info = True)
