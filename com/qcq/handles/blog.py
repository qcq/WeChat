#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018��12��4��

@author: chuanqin
'''
""" Basic blog using webpy 0.3 """
import os
import sys
import web
import com.qcq.const.model as model


### Templates
t_globals = {
    'datestr': web.datestr
}

renderOfBlog = web.template.render(os.path.dirname(os.path.abspath(sys.argv[0])) + '/../templates/', base = 'blog_base', globals=t_globals)


class Index:

    def GET(self):
        """ Show page """
        posts = model.get_posts()
        return renderOfBlog.blog_index(posts)


class View:
    
    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        return renderOfBlog.blog_view(post)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            size=30,
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull, 
            rows=30, cols=80,
            description="Post content:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return renderOfBlog.blog_new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return renderOfBlog.blog_new(form)
        model.new_post(form.d.title, form.d.content)
        raise web.seeother('/blog')


class Delete:
    
    def POST(self, id):
        model.del_post(int(id))
        raise web.seeother('/blog')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return renderOfBlog.blog_edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return renderOfBlog.blog_edit(post, form)
        model.update_post(int(id), form.d.title, form.d.content)
        raise web.seeother('/blog')