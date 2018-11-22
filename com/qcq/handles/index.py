#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018��11��22��

@author: chuanqin
'''
import sys
import web

render = web.template.render(sys.argv[0] + '../templates/')

class index:
    def GET(self):
        i = web.input(name=None)
        return render.index(i.name)