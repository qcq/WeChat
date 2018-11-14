#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import time


class Msg(object):

    def __init__(self, toUserName, fromUserName):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())

    def send(self):
        return "success"


class TextMsg(Msg):

    def __init__(self, toUserName, fromUserName, content):
        Msg.__init__(self, toUserName, fromUserName)
        self.__dict['Content'] = content

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
        return XmlForm.format(**self.__dict)


class ImageMsg(Msg):

    def __init__(self, toUserName, fromUserName, mediaId):
        Msg.__init__(self, toUserName, fromUserName)
        self.__dict['MediaId'] = mediaId

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
        return XmlForm.format(**self.__dict)
