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

from poster.streaminghttp import register_openers
import poster.encode

import com.qcq.const.webconst as webconst
import com.qcq.utils as utils


class Media(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        register_openers()
        self.__leftTime = 0
        self.__picturesPath = u"%s%s" % (
            os.path.dirname(sys.argv[0]), u'../pictures/')

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

    def __updateDatabase(self):
        for picture in utils.findFilesEndsWith(self.__picturesPath, u'JPG'):
            pictureName = os.path.basename(picture).split('.')[0]
            with webconst.db.transaction():
                myvar = dict(name = pictureName)
                selectResult = list(webconst.getPictureByName(pictureName))
                if selectResult:
                    timeLapses = datetime.datetime.utcnow() - \
                        selectResult[0]['created']
                    timeLapses = timeLapses.days * 24 * 60 * 60 + timeLapses.seconds
                    if timeLapses >= 3 * 24 * 60 * 60:
                        logging.info('updating the %s because of 3 days will '
                            'cause picture unavailable%s'
                            % (pictureName, datetime.datetime.utcnow()))
                        result = json.loads(self.upload(webconst.accessToken,
                            picture, u'image'), encoding = 'utf-8')
                        webconst.updatePicture(pictureName, result[u'media_id'], result[u'created_at'])
                    else:
                        logging.info('database already has %s info, no need '
                            'to update the database. time Lapses %s/%s seconds.'
                            % (pictureName, timeLapses, 3 * 24 * 60 * 60))
                else:
                    result = json.loads(self.upload(webconst.accessToken,
                        picture, u'image'), encoding = 'utf-8')
                    webconst.insertPicture(pictureName, picture, result[u'media_id'], result[u'created_at'])
                    logging.info('insert item %s in database in %s'
                        % (pictureName, datetime.datetime.utcnow()))

    def run(self):
        while(True):
            if webconst.accessToken:
                if self.__leftTime > 0:
                    time.sleep(60)
                    self.__leftTime -= 60
                else:
                    self.__updateDatabase()
                    self.__leftTime = 60 * 60
            else:
                time.sleep(5)
