#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月6日

@author: chuanqin
'''
import web

from com.qcq.handles.add import Add
from com.qcq.handles.blog import Delete as blogDelete
from com.qcq.handles.blog import Edit as blogEdit
from com.qcq.handles.blog import Index as blogIndex
from com.qcq.handles.blog import New as blogNew
from com.qcq.handles.blog import View as blogView
from com.qcq.handles.handle import Handle
from com.qcq.handles.index import Index, Delete
from com.qcq.handles.sessions import Login

urls = (
    '/', 'Index',
    '/add', 'Add',
    '/wx', 'Handle',
    '/del/(\d+)', 'Delete',
    '/blog', 'blogIndex',
    '/blog_view/(\d+)', 'blogView',
    '/blog_new', 'blogNew',
    '/blog_delete/(\d+)', 'blogDelete',
    '/blog_edit/(\d+)', 'blogEdit',
    '/login', 'Login',
    '/reset', 'Reset',
)

app = web.application(urls, globals())
