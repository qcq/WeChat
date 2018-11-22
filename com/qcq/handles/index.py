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
db = web.database(dbn='postgres', user='postgres', host = "172.17.0.4", pw='root', db='ebook')

class Index:
    def GET(self):
        webData = web.input(name=None)
        return render.index(webData.name, db.select('todo'))