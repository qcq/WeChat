#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月22日

@author: chuanqin
'''

import web

import com.qcq.const.webconst as webconst


class ToDo:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
                         description = "I need to:"),
        web.form.Button('Add todo'),
    )

    def GET(self):
        """ Show page """
        todos = webconst.getTodos()
        form = self.form()
        return webconst.render.todo(todos, form)

    def POST(self):
        """ Add new entry """
        form = self.form()
        if not form.validates():
            todos = webconst.getTodos()
            return webconst.render.todo(todos, form)
        webconst.newTodo(form.d.title)
        raise web.seeother('/todo')


class Delete:

    def POST(self, id):
        """ Delete based on ID """
        id = int(id)
        webconst.delTodo(id)
        raise web.seeother('/todo')


class Add:

    def POST(self):
        i = web.input()
        webconst.db.insert('todo', title = i.title)
        raise web.seeother('/todo')
