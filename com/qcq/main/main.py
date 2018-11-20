#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import web
from com.qcq.handles.handle import Handle
import com.qcq.access_token as access_token

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    t = access_token.Token()
    t.start()
    t.join()
    app = web.application(urls, globals())
    app.run()
