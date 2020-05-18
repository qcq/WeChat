#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2019-9-15

@author: chuanqin
'''

import logging
import web
import threading
from com.qcq.config.config import settings
import urllib2
import json
import time
import com.qcq.const.webconst as webconst


class BaiDu(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # here should query the database to get the sleep time. if has no this item,
        # or this token expired, should warn in log, the user need to re-acquire this token.
        self._left_time = 0
        self.__updateDatabase__()

    '''
    you have to go
    https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=API_KEY&redirect_uri=http://47.105.187.44/baidu&scope=basic,netdisk&display=page
    here will need you click then, redirect to here with get, then can get the code.
    by which can get access code.
    reference: https://developer.baidu.com/newwiki/dev-wiki/fu-lu.html?t=1557733846879
    https://pan.baidu.com/union/document/entrance#授权流程

    may be here can start a thread to refresh the token
    '''

    def GET(self):
        """ Show page
        the period of validity of code is 10m;
        period of validity of access token is 30d;
        period of validity of refresh token is 10y;
        """
        data = web.input()
        display_str = ''
        if len(data) != 0:
            if data.code:
                display_str = 'get code %s, ' % data.code
                url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type='\
                    'authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' % (
                    data.code, settings.get('baidu', 'apiKey'), settings.get('baidu', 'secretKey'),
                    settings.get('baidu', 'redirect_uri'))

                display_str = display_str + url
                reponse = urllib2.urlopen(url)
                reponse_str = reponse.read()
                result = json.loads(reponse_str)
                logging.info('recoding the request the grant to baidu api with reponse:%s' % json.dumps(result))

                display_str = display_str + '\nexpires_in: %s, refresh_token: %s, access_token: %s' % (
                    result['expires_in'], result['refresh_token'], result['access_token']
                )
                with webconst.db.transaction():
                    if not webconst.getAccessToken('baidu'):
                        logging.info('will insert the access token, refresh token in databse.')
                        webconst.inserAccessToken('baidu', result['access_token'],
                            result['refresh_token'], result['expires_in'], int(time.time()))
                    else:
                        logging.info('will update the access token, refresh token in databse.')
                        webconst.updateAccessToken('baidu', result['access_token'],
                            result['refresh_token'], result['expires_in'], int(time.time()))

        return display_str


    def __updateDatabase__(self):
        '''
        In this function will do below:
        refresh the token, then update it to database.
        '''
        with webconst.db.transaction():
            result = webconst.getAccessToken('baidu')
            if not result:
                logging.warn('please authorize the right first manual.')
                self._left_time = 60 * 60
                return
            refresh_token = ''
            for item in result:
                access_token, refresh_token, expires_in, created_at = item.access_token, \
                    item.refresh_token, item.expires_in, item.created_at
            if time.time() - float(created_at) >= float(expires_in) - 60:
                # here will retrieve the new access_token with refresh_token
                # reference link: https://developer.baidu.com/newwiki/dev-wiki/kai-fa-wen-dang.html?t=1557733846879
                url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type='\
                    'refresh_token&refresh_token=%s&client_id=%s&client_secret=%s' % (
                    refresh_token, settings.get('baidu', 'apiKey'), settings.get('baidu', 'secretKey'))
                logging.info('baidu url request %s' % url)
                result = json.loads(urllib2.urlopen(url).read())
                if 'error' in result:
                    logging.error('when request to baidu, error happened %s will retry in 60s' % result)
                    self._left_time = 60
                    return
                logging.info('current info of baidu %s'%result)
                webconst.updateAccessToken(
                    'baidu', result['access_token'], result['refresh_token'], result['expires_in'], time.time())
                self._left_time = 0
            else:
                self._left_time = int(float(expires_in)) - int(time.time() - int(float(created_at))) - 60
                logging.info('taking into sleep:%s'%self._left_time)


    def run(self):
        while(True):
            if self._left_time > 0:
                time.sleep(self._left_time)
                self._left_time = 0
            else:
                rLock = threading.RLock()  # RLock对象
                rLock.acquire()
                self.__updateDatabase__()
                rLock.release()

