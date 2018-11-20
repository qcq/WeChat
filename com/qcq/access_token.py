#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import urllib
import json
import threading
import time

accessToken = ''

class Token(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):
        global accessToken
        appId = "wxc8e1042108b2b99b"
        appSecret = "90fb2ccd466038eb5ddb996473893658"
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(str(urlResp.read()))
        accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def run(self):
        while(True):
            global accessToken
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                rLock = threading.RLock()  #RLock对象
                self.__real_get_access_token()
                print 'trying update the token:', accessToken, ' with time left:', self.__leftTime
                rLock.acquire()


#Token().get_access_token()
