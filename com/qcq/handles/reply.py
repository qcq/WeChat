#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import time
import logging


class Msg(object):

    def __init__(self, toUserName, fromUserName):
        self.dict = dict()
        self.dict['ToUserName'] = toUserName
        self.dict['FromUserName'] = fromUserName
        self.dict['CreateTime'] = int(time.time())

    def send(self):
        return "success"


class TextMsg(Msg):

    def __init__(self, toUserName, fromUserName, content):
        Msg.__init__(self, toUserName, fromUserName)
        self.dict['Content'] = content
        logging.info('reply text message: %s' % content)

    def send(self):
        XmlForm = u"""
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.dict)


class ImageMsg(Msg):

    def __init__(self, toUserName, fromUserName, mediaId):
        Msg.__init__(self, toUserName, fromUserName)
        self.dict['MediaId'] = mediaId
        logging.info('reply the image media id: %s' % mediaId)

    def send(self):
        XmlForm = u"""
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.dict)
