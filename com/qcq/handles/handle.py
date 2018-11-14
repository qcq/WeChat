#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''
import hashlib
import web
import com.qcq.handles.receive as receive
import com.qcq.handles.reply as reply


class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return u"hello, baby. are you there, I have to say I love you, I am very glad you are here with me for a whole life. It is my honer to have you in my life, in my hug.\n the greatest thing in this world is - hug you in my chest, and kiss you. �����Ұ��㡣"
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
            print 'Exception happened:', Argument
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    return self.__dealTextMessage__(recMsg).send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    return reply.ImageMsg(toUser, fromUser, mediaId).send()
                if recMsg.MsgType == 'event':
                    content = u'欢迎你关注我的公众号，你一定是我的老朋友，我有酒你有故事吗。'
                    return reply.TextMsg(toUser, fromUser, content).send()
                else:
                    return reply.Msg(toUser, fromUser).send()
            else:
                print "暂且不处理"
                return reply.Msg(toUser, fromUser).send()
        except Exception, Argment:
            print 'Exception happened:', Argment
            return Argment

    def __dealTextMessage__(self, recMsg):
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        receiveContent = recMsg.Content
        if u'你' in receiveContent:
            mediaId = u'us79WMrDF_ujGvrA5fvMnAlawfw27AWsngXo07WQIuJqdiSApFfACo4Gi3HWHqSR'
            return reply.ImageMsg(toUser, fromUser, mediaId)
        else:
            content = u"你好，我是你的老朋友，这是我开发的公众号。准备提供电子书服务，希望你喜欢。"
            return reply.TextMsg(toUser, fromUser, content)

