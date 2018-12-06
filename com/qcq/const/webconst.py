#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on Nov 23, 2018

@author: qinchuanqing
'''
import os
import sys

import web

render = web.template.render(os.path.dirname(
    os.path.abspath(sys.argv[0])) + '/../templates/', base = 'base')
db = web.database(dbn = 'postgres', user = 'postgres',
    host = "172.17.0.2", pw = 'root', db = 'ebook')
accessToken = ''
store = web.session.DBStore(db, 'sessions')


def get_todos():
    return db.select('todo', order = 'id')


def new_todo(text):
    db.insert('todo', title = text)


def del_todo(id):
    db.delete('todo', where = "id=$id", vars = locals())


def getPictureByName(name):
    return db.select('pictures', where = "name=$name", vars = locals())
