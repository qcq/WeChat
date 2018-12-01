#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''
import hashlib
import logging
import traceback

import web

import com.qcq.const.message as message
import com.qcq.const.webconst as webconst
import com.qcq.handles.receive as receive
import com.qcq.handles.reply as reply

dealing_message = []


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

            verifyList = [token, timestamp, nonce]
            verifyList.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, verifyList)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            print 'Exception happened:', traceback.print_exc()
            return Argument

    def POST(self):
        try:
            webData = web.data()
            logging.info('%s%s' % ("Handle Post webdata is ", webData))
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # dealing with repeat deal with message
                if webData not in dealing_message:
                    dealing_message.append(webData)
                else:
                    return reply.Msg(toUser, fromUser).send()
                if recMsg.MsgType == 'text':
                    return self.__dealTextMessage__(recMsg).send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    return reply.ImageMsg(toUser, fromUser, mediaId).send()
                if recMsg.MsgType == 'event':
                    return reply.TextMsg(toUser, fromUser, message.subscription_content).send()
                else:
                    return reply.Msg(toUser, fromUser).send()
            else:
                print "暂且不处理"
                return reply.Msg(toUser, fromUser).send()
            dealing_message.remove(webData)
        except Exception, Argment:
            print 'Exception happened:', traceback.print_exc()
            logging.warn('Exception happened:%s' % traceback.print_exc(), exc_info = True, stack_info = True)
            return Argment

    def __dealTextMessage__(self, recMsg):
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        receiveContent = recMsg.Content
        media_id_temp = webconst.getPictureByName(receiveContent)[0][u'media_id']
        if media_id_temp:
            return reply.ImageMsg(toUser, fromUser, media_id_temp['media_id'])
        elif u'在吗' in receiveContent:
            return reply.TextMsg(toUser, fromUser, u'我在这里一直等你。')
        elif u'链接' in receiveContent:
            return reply.TextMsg(toUser, fromUser, message.hyeper_link_content % (toUser))
        else:
            return reply.TextMsg(toUser, fromUser, message.default_content)
