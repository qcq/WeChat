#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018Äê12ÔÂ4ÈÕ

@author: chuanqin
'''
import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('./config.ini')
print settings.sections()
print settings.get(u'email section', 'email user')