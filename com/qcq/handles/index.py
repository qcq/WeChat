#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018��11��22��

@author: chuanqin
'''

import web
import com.qcq.const.webconst as webconst


class Index:

    def GET(self):
        webData = web.input(name=None)
        return webconst.render.index(webData.name, webconst.db.select('todo'))
