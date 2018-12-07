#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月6日

@author: chuanqin
'''
import hashlib
import logging

import web

from com.qcq.const import webconst
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
    '/register', 'Register'
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
        ident = db.select('users', where = 'name=$name', vars = locals())
        if not ident:
            logging.info('user with name %s not exist, will direct to register page.' % name)
            raise web.seeother('/register')
        try:
            if hashlib.sha1("sAlT754-" + passwd).hexdigest() == ident['password']:
                session.login = 1
                session.privilege = ident['privilege']
                render = create_render(session.privilege)
                return render.todo()
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


class Reset:

    def GET(self):
        session.login = 0
        session.kill()
        render = create_render(session.privilege)
        return render.logout()


vpass = web.form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = web.form.regexp(r".*@.*", "must be a valid email address")

register_form = web.form.Form(
    web.form.Textbox("username", description = "Username"),
    web.form.Textbox("email", vemail, description = "E-Mail"),
    web.form.Password("password", vpass, description = "Password"),
    web.form.Password("password2", description = "Repeat password"),
    web.form.Button("submit", type = "submit", description = "Register"),
    validators = [
        web.form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)


class Register:

    def GET(self):
        render = create_render(session.privilege)
        f = register_form()
        return render.register(f)

    def POST(self):
        render = create_render(session.privilege)
        f = register_form()
        if not f.validates():
            return render.register(f)
        data = web.input()
        username, passwd, emailAddress = data.username, data.password, data.email
        webconst.insertUser(username, hashlib.sha1("sAlT754-" + passwd).hexdigest(), emailAddress)
        logging.info('inser user: %s into database' % username)
