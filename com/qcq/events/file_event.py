#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2019年9月11日

@author: chuanqin
'''


from enum import Enum


class FileEventType(Enum):
    CREATE = 1
    MOVE = 2
    DELETE = 3

class FileEvent:
    # Additional fields and methods if needed
    def __init__(self, event_type, src, dst):
        self._event_type = event_type
        self._src = src
        self._dst = dst
