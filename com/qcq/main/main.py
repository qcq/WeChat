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

import web

import com.qcq.access_token as access_token
from com.qcq.handles.add import Add
from com.qcq.handles.handle import Handle
from com.qcq.handles.index import Index, Delete
import com.qcq.media.media as media
from com.qcq.handles.blog import Index as blogIndex
from com.qcq.handles.blog import View as blogView
from com.qcq.handles.blog import New as blogNew
from com.qcq.handles.blog import Delete as blogDelete
from com.qcq.handles.blog import Edit as blogEdit
from logging import FileHandler

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(filename)s-%(funcName)s:%(lineno)d:%(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
LOG_FILE_NAME = r'/home/chuanqin/log.txt'


def shutdown(signum, frame):
    print 'You are in the process of shutting down the server.', signum, frame
    logging.info('The system is going down by the ctrl+c signal.')
    sys.exit()


urls = (
    '/', 'Index',
    '/add', 'Add',
    '/wx', 'Handle',
    '/del/(\d+)', 'Delete',
    '/blog', 'blogIndex',
    '/blog_view/(\d+)', 'blogView',
    '/blog_new', 'blogNew',
    '/blog_delete/(\d+)', 'blogDelete',
    '/blog_edit/(\d+)', 'blogEdit',
)

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
        logging.info("server's get access token thread is running in Daemon mode.")
        uploadPicture = media.Media()
        uploadPicture.setDaemon(True)
        uploadPicture.start()
        logging.info("server is running to upload pictures to tencent.")
        app = web.application(urls, globals())
        logging.info("server is ready to provide the service.")

        app.run()
    except Exception, exc:
        print exc, traceback.print_exc()
