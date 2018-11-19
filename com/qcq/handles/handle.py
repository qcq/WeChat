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
import com.qcq.const.media_id as media_id
import com.qcq.const.message as message
import com.qcq.media.media as media
import com.qcq.access_token as access_token
import traceback


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
                    return reply.TextMsg(toUser, fromUser, message.subscription_content).send()
                else:
                    return reply.Msg(toUser, fromUser).send()
            else:
                print "暂且不处理"
                return reply.Msg(toUser, fromUser).send()
        except Exception, Argment:
            print 'Exception happened:', traceback.print_exc()
            return Argment

    def __dealTextMessage__(self, recMsg):
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        receiveContent = recMsg.Content
        if u'你' in receiveContent or u'我' in receiveContent:
            return reply.ImageMsg(toUser, fromUser, media_id.media_id_me)
        elif u'结婚' in receiveContent:
            return reply.ImageMsg(toUser, fromUser, media_id.media_id_married)
        elif u'风景' in receiveContent:
            self.__tryToUploadImage(media_id.married_image_path)
            return reply.ImageMsg(toUser, fromUser, media_id.media_id_married)
        else:
            return reply.TextMsg(toUser, fromUser, message.default_content)
        
    def __tryToUploadImage(self, path):
        myMedia = media.Media()
        accessToken = access_token.Basic().get_access_token()
        mediaType = "image"
        print myMedia.uplaod(accessToken, path, mediaType)