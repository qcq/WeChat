#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on Nov 23, 2018

@author: qinchuanqing
'''
import datetime
import os
import sys

import web

render = web.template.render(os.path.dirname(
    os.path.abspath(sys.argv[0])) + '/../templates/', base = 'base')
db = web.database(dbn = 'postgres', user = 'postgres',
    host = "172.17.0.2", pw = 'root', db = 'ebook')
accessToken = ''
store = web.session.DBStore(db, 'sessions')


def getTodos():
    return db.select('todo', order = 'id')


def newTodo(text):
    db.insert('todo', title = text)


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
    return db.select('pictures', where = "name=$name", vars = locals())


def updatePicture(name, media_id, created_at):
    db.update('pictures', where = "name=$name", vars = locals(), media_id = media_id,
         created_at = created_at, created = datetime.datetime.utcnow())


def insertPicture(pictureName, path, media_id, created_at):
    db.insert('pictures', name = pictureName, path = path, media_id = media_id,
        created_at = created_at, created = datetime.datetime.utcnow())


def getUserByName(name):
    return db.select('users', where = 'name=$name', vars = locals())


def insertUser(username, passwd, emailAddress):
    db.insert('users', name = username, password = passwd, email = emailAddress)
