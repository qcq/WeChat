#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import logging
import signal
import sys

import web

import com.qcq.access_token as access_token
from com.qcq.handles.add import Add
from com.qcq.handles.handle import Handle
from com.qcq.handles.index import Index, Delete
import com.qcq.media.media as media

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(filename)s-%(funcName)s:%(lineno)d:%(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FILE_NAME = r'/home/chuanqin/log.txt'


def quit(signum, frame):
    print 'You are in the process of shutting down the server.'
    sys.exit()


urls = (
    '/', 'Index',
    '/add', 'Add',
    '/wx', 'Handle',
    '/del/(\d+)', 'Delete'
)

if __name__ == '__main__':
    try:
        logging.basicConfig(filename = LOG_FILE_NAME, level = logging.INFO, format = LOG_FORMAT, datefmt = DATE_FORMAT)
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        t = access_token.Token()
        t.setDaemon(True)
        t.start()
        logging.info("server's get access token thread is runing in Daemon mode.")
        uploadPicture = media.Media()
        uploadPicture.setDaemon(True)
        uploadPicture.start()
        logging.info("server is running to upload pictures to tencent.")
        app = web.application(urls, globals())
        logging.info("server is ready to provide the service.")

        app.run()
    except Exception, exc:
        print exc
