#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''
import json
import logging
import os
import sys
import threading
import time
import urllib2

import poster.encode
from poster.streaminghttp import register_openers

import com.qcq.const.media_id as media_id
import com.qcq.const.webconst as webconst
import com.qcq.utils as utils


class Media(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        register_openers()
        self.__leftTime = 0
        self.__picturesPath = u"%s%s" % (os.path.dirname(sys.argv[0]), u'../pictures/')

    def __getPictureFiles(self):
        picturesData = []
        for picture in utils.findFilesEndsWith(self.__picturesPath, u'JPG'):
            temp = {}
            name = os.path.basename(picture).split('.')[0]
            temp[u'name'] = name
            temp[u'path'] = picture
            temp[u'media_id'] = u''
            picturesData.append(temp)

    def upload(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        return urlResp.read()

    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (accessToken, mediaId)
        urlResp = urllib2.urlopen(postUrl)

        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print jsonDict
        else:
            mediaBuffer = urlResp.read()  # 素材的二进制
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(mediaBuffer)
            print "get successful"

    def run(self):
        while(True):
            if webconst.accessToken:
                if self.__leftTime > 0:
                    time.sleep(60)
                    self.__leftTime -= 60
                else:
                    for picture in utils.findFilesEndsWith(self.__picturesPath, u'JPG'):
                        name = os.path.basename(picture).split('.')[0]
                    '''
                    for picture in utils.findFilesEndsWith(picturesPath, u'JPG'):
                        temp = {}
                        name = os.path.basename(picture).split('.')[0]
                        temp[u'name'] = name
                        temp[u'path'] = picture
                        temp[u'media_id'] = u''
                        picturesData.append(temp)
                    # TODO, need to inser the item in database, if exist, should update them,
                    then logic should be:
                    1. query whether item exist:
                        if not, db.insert
                        else :
                            if time is in effect range, just continue
                            else db.update the item.
                    2 need consider the transaction operation here.
                    '''
                    for item in media_id.picturesData:
                        result = json.loads(self.upload(webconst.accessToken, item[u'path'], u'image'), encoding = 'utf-8')
                        item[u'media_id'] = result[u'media_id']
                        item[u'created_at'] = result[u'created_at']
                        print 'upload image', item, result
                        logging.info("%s %s %s" % ('upload image', item, result))
                        self.__leftTime = 3 * 24 * 60 * 60
            else:
                time.sleep(1)
