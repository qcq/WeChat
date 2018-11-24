#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on Nov 23, 2018

@author: qinchuanqing
'''

import com.qcq.const.webconst as webconst
import web


class Add:

    def POST(self):
        i = web.input()
        n = webconst.db.insert('todo', title = i.title)
        raise web.seeother('/')
