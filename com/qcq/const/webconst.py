#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on Nov 23, 2018

@author: qinchuanqing
'''
import datetime
import os
import sys
'''
# found one issue, which the web.db print the sql statement in wrong format of
# chinese, which first thought caused by the encoding of sys module, in final proves
# its not this question, take the link: https://groups.google.com/forum/#!topic/python-cn/lm4I6Ti3SxA
# as reference. finally solved by replace where = "name=$name" with where = u"name = '%s'" % name.

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
'''

import web

render = web.template.render(os.path.dirname(
    os.path.abspath(sys.argv[0])) + '/../templates/', base = 'base')
db = web.database(dbn = 'postgres', user = 'postgres',
    host = "172.17.0.2", pw = 'root', db = 'ebook')#, charset='utf8')
accessToken = ''
store = web.session.DBStore(db, 'sessions')


def getTodos(name):
    return db.select('todo', order = 'id', where = u"name='%s'" % name)#, vars = locals())


def newTodo(text, name):
    db.insert('todo', title = text, name = name)


def delTodo(id):
    db.delete('todo', where = "id=$id", vars = locals())


def getPosts():
    return db.select('entries', order = 'id DESC')


def getPost(id):
    try:
        return db.select('entries', where = 'id=$id', vars = locals())[0]
    except IndexError:
        return None


def newPost(title, text):
    db.insert('entries', title = title, content = text,
                       posted_on = datetime.datetime.utcnow())


def delPost(id):
    db.delete('entries', where = "id=$id", vars = locals())


def updatePost(id, title, text):
    db.update('entries', where = "id=$id", vars = locals(),
                       title = title, content = text)


def getPictureByName(name):
    return db.select('pictures', where = u"name='%s'" % name)


def updatePicture(name, media_id, created_at):
    db.update('pictures', where = "name=$name", vars = locals(), media_id = media_id,
         created_at = created_at, created = datetime.datetime.utcnow())


def insertPicture(pictureName, path, media_id, created_at):
    db.insert('pictures', name = pictureName, path = path, media_id = media_id,
        created_at = created_at, created = datetime.datetime.utcnow())


def deletePicture(pictureName):
    db.delete('pictures', where = "name='%s'" % pictureName)


def getUserByName(name):
    return db.select('users', where = 'name=$name', vars = locals())


def insertUser(username, passwd, emailAddress):
    db.insert('users', name = username, password = passwd, email = emailAddress)
