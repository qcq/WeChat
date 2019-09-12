#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''
from __future__ import with_statement

import datetime
import json
import logging
import os
import sys
import threading
import time
import urllib2
from pyeventbus import *

from poster.streaminghttp import register_openers
import poster.encode

import com.qcq.const.webconst as webconst
import com.qcq.utils as utils
from com.qcq.events.file_event import *


class Media(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        register_openers()
        self.__leftTime = 0
        self.__picturesPath = u"%s%s" % (
            os.path.dirname(sys.argv[0]), u'../pictures/')
        self.__DayInSeconds = 3 * 24 * 60 * 60

    def upload(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (
            accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        return urlResp.read()

    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (
            accessToken, mediaId)
        urlResp = urllib2.urlopen(postUrl)

        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) \
            or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print jsonDict
        else:
            mediaBuffer = urlResp.read()  # 素材的二进制
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(mediaBuffer)
            print "get successful"

    def register(self, bInstance):
        PyBus.Instance().register(bInstance, self.__class__.__name__)

    @subscribe(threadMode=Mode.BACKGROUND, onEvent=FileEvent)
    def readEventFromA(self, event):
        logging.info('received event type:%s, src: %s, dst: %s' %
                     (event._event_type, event._src, event._dst))
        if event._event_type == FileEventType.CREATE:
            self.__newPictureFound__(event._src)
        elif event._event_type == FileEventType.MOVE:
            self.__pictureNameChaned__(event._src, event._dst)
        elif event._event_type == FileEventType.DELETE:
            self.__pictureDelete__(event._src)
        else:
            logging.warn('not defined file event happened.')

    def __newPictureFound__(self, picture):
        pictureName = os.path.basename(picture).split('.')[0]
        with webconst.db.transaction():
            if not list(webconst.getPictureByName(pictureName)):
                result = json.loads(self.upload(webconst.accessToken, picture,
                    u'image'), encoding='utf-8')
                if 'errcode' in result:
                    logging.warn('can not upload the %s to server with error %s' % (picture, result))
                    return
                '''
                https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/New_temporary_materials.html
                reference the link, temporary material has time < 3-days limit, size <=2M.
                '''
                webconst.insertPicture(pictureName, picture, result[u'media_id'], result[u'created_at'])
                logging.info('insert item %s in database in %s'
                    % (pictureName, datetime.datetime.utcnow()))

    def __pictureNameChaned__(self, src, dst):
        self.__pictureDelete__(src)
        self.__newPictureFound__(dst)

    def __pictureDelete__(self, picture):
        pictureName = os.path.basename(picture).split('.')[0]
        webconst.deletePicture(pictureName)

    def __updateDatabase(self):
        for picture in utils.findFilesEndsWith(self.__picturesPath, u'JPG', u'PNG'):
            pictureName = os.path.basename(picture).split('.')[0]
            with webconst.db.transaction():
                selectResult = list(webconst.getPictureByName(pictureName))
                if selectResult:
                    timeLapses = datetime.datetime.utcnow() - \
                        selectResult[0]['created']
                    timeLapses = timeLapses.days * self.__DayInSeconds + timeLapses.seconds
                    if timeLapses >= 3 * self.__DayInSeconds:
                        logging.info('updating the %s because of 3 days will '
                            'cause picture unavailable%s'
                            % (pictureName, datetime.datetime.utcnow()))
                        result = json.loads(self.upload(webconst.accessToken,
                            picture, u'image'), encoding = 'utf-8')
                        webconst.updatePicture(pictureName, result[u'media_id'], result[u'created_at'])
                    else:
                        logging.info('database already has %s info, no need '
                            'to update the database. time Lapses %s/%s seconds.'
                            % (pictureName, timeLapses, 3 * self.__DayInSeconds))
                else:
                    self.__newPictureFound__(picture)

    def run(self):
        while(True):
            '''
            here will take 60min as unit to check whether the picture need to update to tencent,
            which has disadvantage —— can not upload new add picture as new service,  and may be
            cause some old picture unavailable, here need to improve.
            '''
            if webconst.accessToken:
                if self.__leftTime > 0:
                    time.sleep(60)
                    self.__leftTime -= 60
                else:
                    self.__updateDatabase()
                    self.__leftTime = 60 * 60
            else:
                time.sleep(5)
