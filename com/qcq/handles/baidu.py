#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2019-9-15

@author: chuanqin
'''

import web
from com.qcq.config.config import settings
import urllib2
import json

class BaiDu:

    '''
    you have to go
    https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=API_KEY&redirect_uri=http://47.105.187.44/baidu&scope=basic,netdisk&display=page
    here will need you click then, redirect to here with get, then can get the code.
    by which can get access code.
    reference: https://developer.baidu.com/newwiki/dev-wiki/fu-lu.html?t=1557733846879
    https://pan.baidu.com/union/document/entrance#授权流程
    '''

    def GET(self):
        """ Show page """
        data = web.input()
        display_str = ''
        if len(data) != 0:
            if data.code:
                display_str = 'get code %s' % data.code
                url = r'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s&redirect_uri=%s' % (
                    data.code, settings.get('baidu', 'apiKey'), settings.get('baidu', 'secretKey'), settings.get('baidu', 'redirect_uri'))

                display_str = display_str + url
                reponse = urllib2.urlopen(url)
                reponse_str = reponse.read()
                result = json.loads(reponse_str, encoding='utf-8')

                display_str = display_str + '\nexpires_in: %s, refresh_token: %s, access_token: %s' % (
                    result['expires_in'], result['refresh_token'], result['access_token']
                )

        return display_str



