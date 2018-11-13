#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''
import hashlib
import web

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return u"hello, baby. are you there, I have to say I love you, I am very glad you are here with me for a whole life. It is my honer to have you in my life, in my hug.\n the greatest thing in this world is - hug you in my chest, and kiss you. 宝宝我爱你。"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "qcq"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument