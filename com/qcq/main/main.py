#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import web
from com.qcq.handles.handle import Handle

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()