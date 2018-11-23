#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on Nov 23, 2018

@author: qinchuanqing
'''
import os
import sys

import web

render = web.template.render(os.path.dirname(sys.argv[0]) + '../templates/')
db = web.database(dbn='postgres', user='postgres', host="172.17.0.4", pw='root', db='ebook')
