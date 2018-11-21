#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import web
import sys
from com.qcq.handles.handle import Handle
import com.qcq.access_token as access_token
import signal


def quit(signum, frame):
    print 'You are in the process of shutting down the server.'
    sys.exit()


urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        t = access_token.Token()
        t.setDaemon(True)
        t.start()
        app = web.application(urls, globals())
        app.run()
    except Exception, exc:
        print exc
