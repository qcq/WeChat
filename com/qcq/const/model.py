#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月4日

@author: chuanqin
'''
import datetime

import com.qcq.const.webconst as webconst


def get_posts():
    return webconst.db.select('entries', order='id DESC')


def get_post(id):
    try:
        return webconst.db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None


def new_post(title, text):
    webconst.db.insert('entries', title=title, content=text,
                       posted_on=datetime.datetime.utcnow())


def del_post(id):
    webconst.db.delete('entries', where="id=$id", vars=locals())


def update_post(id, title, text):
    webconst.db.update('entries', where="id=$id", vars=locals(),
                       title=title, content=text)
