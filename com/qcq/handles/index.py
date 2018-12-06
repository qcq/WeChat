#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月6日

@author: chuanqin
'''

import web


class Index:

    def GET(self):
        raise web.seeother('/login')

