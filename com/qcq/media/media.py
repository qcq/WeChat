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
import traceback
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
        self._left_time = 0

        self._DayInSeconds = 24 * 60 * 60

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
    def readEventFromPicturePathHandler(self, event):
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
        # need to add limit, judge the filesize should less than 2M, if not delete it.
        pictureName = os.path.basename(picture).split('.')[0]
        with webconst.db.transaction():
            if not webconst.getPictureByName(pictureName):
                try:
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
                except Exception, exc:
                    logging.warn('Exception happened:%s' % traceback.print_exc(), exc_info=True)

    def __pictureNameChaned__(self, src, dst):
        self.__pictureDelete__(src)
        self.__newPictureFound__(dst)

    def __pictureDelete__(self, picture):
        pictureName = os.path.basename(picture).split('.')[0]
        webconst.deletePicture(pictureName)

    def __updateDatabase__(self):
        '''
        This function will update to:
        '''
        search_result = webconst.getOldestPictureCreatedTime()
        if search_result:
            for item in search_result:
                created_at, created_time, name, path = item.created_at, item.created, item.name, item.path
            time_lapses = time.time() - int(created_at)  # int(time.mktime(now.timetuple()))
            if time_lapses >= 3 * self._DayInSeconds:
                logging.info('updating the %s because of 3 days will cause picture unavailable:%s/%s-%s/%s'
                    % (name, created_time, time.time(), datetime.datetime.fromtimestamp(created_at), datetime.datetime.utcnow()))
                if os.path.exists(path):
                    result = json.loads(self.upload(webconst.accessToken, path,
                        u'image'), encoding='utf-8')
                    webconst.updatePicture(name, result[u'media_id'], result[u'created_at'])
                else:
                    # if the picture non-exist any more, delete from database.
                    self.__pictureDelete__(name)
                self.__updateDatabase__()
            else :
                self._left_time = 3 * self._DayInSeconds - time_lapses - 60
                logging.info('no file need to update. take thread sleep %s' % self._left_time)
        else:
            '''
            if has nothing in database, can sleep 3 days, because, only add new picture
            can trigger database has item, one item avaliable in 3 days, so, sleep 3
            days is fine.
            '''
            self._left_time = 3 * self._DayInSeconds - 60
            logging.info('current has no items in database, take sleep %s.' % self._left_time)

    def run(self):
        while(True):
            '''
            here will take 60min as unit to check whether the picture need to update to tencent,
            which has disadvantage —— can not upload new add picture as new service,  and may be
            cause some old picture unavailable, here need to improve.
            improved
            '''
            if webconst.accessToken:
                if self._left_time > 0:
                    time.sleep(self._left_time)
                    self._left_time = 0
                else:
                    rLock = threading.RLock()  # RLock对象
                    rLock.acquire()
                    self.__updateDatabase__()
                    rLock.release()
            else:
                time.sleep(5)
