#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018��12��4��

@author: chuanqin
'''
import os
import sys

import configparser


settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read(os.path.dirname(os.path.abspath(
    sys.argv[0])) + '/../config/config.ini')
print settings.sections()
print settings.get(u'email section', 'email user')
