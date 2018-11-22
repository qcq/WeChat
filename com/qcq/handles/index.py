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

class Index:
    def GET(self):
        i = web.input(name=None)
        return render.index(i.name)