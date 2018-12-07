#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月4日

@author: chuanqin
'''
""" Basic blog using webpy 0.3 """
import os
import sys

import web

import com.qcq.const.webconst as webconst

# ## Templates
t_globals = {
    'datestr': web.datestr
}

renderOfBlog = web.template.render(os.path.dirname(os.path.abspath(
    sys.argv[0])) + '/../templates/', base = 'blog_base', globals = t_globals)


class Index:

    def GET(self):
        """ Show page """
        posts = webconst.getPosts()
        return renderOfBlog.blog_index(posts)


class View:

    def GET(self, id):
        """ View single post """
        post = webconst.getPost(int(id))
        return renderOfBlog.blog_view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull,
                         size = 30,
                         description = "Post title:"),
        web.form.Textarea('content', web.form.notnull,
                          rows = 30, cols = 80,
                          description = "Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return renderOfBlog.blog_new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return renderOfBlog.blog_new(form)
        webconst.newPost(form.d.title, form.d.content)
        raise web.seeother('/blog')


class Delete:

    def POST(self, id):
        webconst.delPost(int(id))
        raise web.seeother('/blog')


class Edit:

    def GET(self, id):
        post = webconst.getPost(int(id))
        form = New.form()
        form.fill(post)
        return renderOfBlog.blog_edit(post, form)

    def POST(self, id):
        form = New.form()
        post = webconst.getPost(int(id))
        if not form.validates():
            return renderOfBlog.blog_edit(post, form)
        webconst.updatePost(int(id), form.d.title, form.d.content)
        raise web.seeother('/blog')
