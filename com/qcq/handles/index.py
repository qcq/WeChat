#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018��11��22��

@author: chuanqin
'''

import web

import com.qcq.const.webconst as webconst


class Index:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
            description = "I need to:"),
        web.form.Button('Add todo'),
    )

    def GET(self):
        """ Show page """
        todos = webconst.get_todos()
        form = self.form()
        return webconst.render.index(todos, form)

    def POST(self):
        """ Add new entry """
        form = self.form()
        if not form.validates():
            todos = webconst.get_todos()
            return webconst.render.index(todos, form)
        webconst.new_todo(form.d.title)
        raise web.seeother('/')


class Delete:

    def POST(self, id):
        """ Delete based on ID """
        id = int(id)
        webconst.del_todo(id)
        raise web.seeother('/')
