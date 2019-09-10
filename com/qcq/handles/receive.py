#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import logging
import xml.etree.ElementTree as ET

def parse_xml(web_data):
    if len(web_data) == 0:
        logging.warn('receive the none message.')
        return None
    xmlData = ET.fromstring(web_data)
    msg_type = xmlData.find('MsgType').text
    if msg_type == 'event':
        return EventMsg(xmlData)
        '''
        event_type = xmlData.find('Event').text
        if event_type == 'CLICK':
            return Click(xmlData)
        #elif event_type in ('subscribe', 'unsubscribe'):
            #return Subscribe(xmlData)
        #elif event_type == 'VIEW':
            #return View(xmlData)
        #elif event_type == 'LOCATION':
            #return LocationEvent(xmlData)
        #elif event_type == 'SCAN':
            #return Scan(xmlData)
        '''
    elif msg_type == 'text':
        return TextMsg(xmlData)
    elif msg_type == 'image':
        return ImageMsg(xmlData)


class Msg(object):

    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text


class TextMsg(Msg):

    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.MsgId = xmlData.find('MsgId').text
        self.Content = xmlData.find('Content').text


class ImageMsg(Msg):

    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.MsgId = xmlData.find('MsgId').text
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text


class EventMsg(Msg):

    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Event = xmlData.find('Event').text
        self.Eventkey = xmlData.find('EventKey').text
