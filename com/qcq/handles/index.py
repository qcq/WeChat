#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018��11��22��

@author: chuanqin
'''
import os
import sys
import web

render = web.template.render(os.path.dirname(sys.argv[0]) + '../templates/')
db = web.database(dbn='postgres', user='postgres', pw='root', db='ebook')

class Index:
    def GET(self):
        webData = web.input(name=None)
        if webData:
            return render.index(webData.name)
        else:
            return render.index(db.select('todo'))