#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import json
import logging
import threading
import time
import urllib

from com.qcq.config.config import settings
import com.qcq.const.webconst as webconst


class Token(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.__accessToken = ''
        self.__leftTime = 0

    def __realGetAccessToken(self):
        appId = settings.get(u'wx', 'appId')
        appSecret = settings.get(u'wx', 'appSecret')
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
            "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(str(urlResp.read()))
        webconst.accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                rLock = threading.RLock()  # RLock对象
                rLock.acquire()
                logging.info('%s%s%s%s' % ('trying update the token:',
                    webconst.accessToken, ' with time left:', self.__leftTime))
                self.__realGetAccessToken()
                logging.info('%s%s%s%s' % ('update the token succeed:',
                    webconst.accessToken, ' with time left:', self.__leftTime))
                rLock.release()
