#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月6日

@author: chuanqin
'''
import hashlib

import web

from com.qcq.const.webconst import render as defaultRender
from com.qcq.const.webconst import store, db
from com.qcq.handles.blog import Delete as blogDelete
from com.qcq.handles.blog import Edit as blogEdit
from com.qcq.handles.blog import Index as blogIndex
from com.qcq.handles.blog import New as blogNew
from com.qcq.handles.blog import View as blogView
from com.qcq.handles.handle import Handle
from com.qcq.handles.index import Index
from com.qcq.handles.todo import Add as todoAdd
from com.qcq.handles.todo import Delete as todoDelete
from com.qcq.handles.todo import ToDo as todoIndex

web.config.debug = False

urls = (
    '/', 'Index',
    '/todo', 'todoIndex',
    '/todo_add', 'todoAdd',
    '/wx', 'Handle',
    '/todo_del/(\d+)', 'todoDelete',
    '/blog', 'blogIndex',
    '/blog_view/(\d+)', 'blogView',
    '/blog_new', 'blogNew',
    '/blog_delete/(\d+)', 'blogDelete',
    '/blog_edit/(\d+)', 'blogEdit',
    '/login', 'Login',
    '/reset', 'Reset',
)

app = web.application(urls, globals())
session = web.session.Session(app, store, initializer = {'uid': 0, 'username': '',
    'current_page': 'index', 'user_role': 'invited', 'login': 0, 'privilege': 0})


def logged():
    if session.login == 1:
        return True
    else:
        return False


def create_render(privilege):
    '''
    if logged():
        if privilege == 0:
            render = web.template.render('templates/reader')
        elif privilege == 1:
            render = web.template.render('templates/user')
        elif privilege == 2:
            render = web.template.render('templates/admin')
        else:
            render = web.template.render('templates/communs')
    else:
        render = web.template.render('templates/communs')
    '''
    return defaultRender


class Login:

    def GET(self):
        if logged():
            render = create_render(session.privilege)
            return '%s' % render.login_double()
        else:
            render = create_render(session.privilege)
            return '%s' % render.login()

    def POST(self):
        name, passwd = web.input().name, web.input().passwd
        ident = db.select('users', where = 'name=$name', vars = locals())[0]
        try:
            if hashlib.sha1("sAlT754-" + passwd).hexdigest() == ident['pass']:
                session.login = 1
                session.privilege = ident['privilege']
                render = create_render(session.privilege)
                return render.login_ok()
            else:
                session.login = 0
                session.privilege = 0
                render = create_render(session.privilege)
                return render.login_error()
        except:
            session.login = 0
            session.privilege = 0
            render = create_render(session.privilege)
            return render.login_error()

