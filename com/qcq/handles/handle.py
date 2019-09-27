#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13日

@author: chuanqin
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#reference https://www.jianshu.com/p/5017d8342dd2
import hashlib
import logging
import traceback

import web
import urllib
import urllib2
import json

import com.qcq.const.message as message
import com.qcq.const.webconst as webconst
import com.qcq.handles.receive as receive
import com.qcq.handles.reply as reply
from com.qcq.config.config import settings

dealing_message = []


class Handle(object):

    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return (u"hello, baby. are you there, I have to say I love you,"
                    " I am very glad you are here with me for a whole life."
                    " It is my honer to have you in my life, in my hug.\n "
                    "the greatest thing in this world is - hug you in my chest, and kiss you.")
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "qcq"

            verifyList = [token, timestamp, nonce]
            verifyList.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, verifyList)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            print 'Exception happened:', traceback.print_exc()
            return Argument

    def POST(self):
        try:
            webData = web.data()
            logging.info("Handle Post webdata is:\n%s" % webData)
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                # dealing with repeat deal with message
                if webData not in dealing_message:
                    dealing_message.append(webData)
                else:
                    return reply.Msg(toUser, fromUser).send()
                if recMsg.MsgType == 'text':
                    return self.__dealTextMessage__(recMsg).send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    return reply.ImageMsg(toUser, fromUser, mediaId).send()
                if recMsg.MsgType == 'event':
                    return reply.TextMsg(toUser, fromUser, message.subscription_content).send()
                else:
                    return reply.Msg(toUser, fromUser).send()
            else:
                print u"暂且不处理"
                return reply.Msg(toUser, fromUser).send()
            dealing_message.remove(webData)
        except Exception, Argment:
            logging.warn('Exception happened:%s' %
                traceback.print_exc(), exc_info = True)
            return Argment

    def __dealTextMessage__(self, recMsg):
        toUser = recMsg.FromUserName
        fromUser = recMsg.ToUserName
        receiveContent = recMsg.Content
        if u'搜书 ' in receiveContent:
            # here will query the database get the access_token, then to baidu query fs_id
            search_result = webconst.getAccessToken('baidu')
            if not search_result:
                return reply.TextMsg(toUser, fromUser, u'不能和百度网盘通信。')
            access_token = search_result[0].access_token
            file_name = self.__parseFileNameFromUserTypes__(receiveContent)
            result = self.__getFsId__(access_token, file_name)
            if not result['list']:
                return reply.TextMsg(toUser, fromUser, u'找不到这本书。')
            fs_ids = self.__filterOutAllFsId__(result['list'])
            if not fs_ids:
                return reply.TextMsg(toUser, fromUser, u"没有收录这本书的mobi、"\
                    u"azw3、epub版本，如有需要请联系楼主添加资源。")
            result = self.__shareBook__(access_token, fs_ids)
            if not result['link']:
                return reply.TextMsg(toUser, fromUser, u'创建分享链接失败。')
            return reply.TextMsg(toUser, fromUser, u'share link:%s with password: 1234' % result['link'])
        media_id_temp = webconst.getPictureByName(receiveContent)
        if media_id_temp:
            return reply.ImageMsg(toUser, fromUser, media_id_temp[0][u'media_id'])
        elif u'在吗' in receiveContent:
            return reply.TextMsg(toUser, fromUser, u'我在这里一直等你来。')
        elif u'待办事项' in receiveContent:
            return reply.TextMsg(toUser, fromUser, message.to_do_list_login)
        elif u'博客' in receiveContent:
            return reply.TextMsg(toUser, fromUser, message.blog)
        else:
            return reply.TextMsg(toUser, fromUser, message.default_content)

    def __getFsId__(self, access_token, name):
        url = "https://pan.baidu.com/rest/2.0/xpan/file?method=search&access_tok"\
            "en=%s&dir=/书籍&key=%s&recursion=1&web=1" % (access_token, name)
        logging.debug('search the file:%s with url %s' % (name, url))
        result = json.loads(urllib2.urlopen(url).read())
        logging.debug('get the fs_id from baidu %s' % json.dumps(result))
        return result

    def __filterOutAllFsId__(self, search_result_of_file):
        # https://pan.baidu.com/union/document/openLink#创建外链
        # fid_list should less than 1000!
        # here define filter, get the file which is not folder, and has the suffix
        # mobi, epub, azw3, and limit to 1000
        return [str(item['fs_id']) for item in search_result_of_file\
            if item['isdir'] == 0 and item['path'].lower().endswith(('.mobi', \
            '.azw3', '.epub'))][0:1000]

    def __shareBook__(self, access_token, fs_ids):
        fs_id_str = ','.join(fs_ids)
        postUrl = 'https://pan.baidu.com/share/set?access_token=%s' % access_token
        data = {'fid_list': '[%s]' % fs_id_str, 'schannel': '4',
                'channel_list': '[]', 'pwd': '1234', 'period': '7'}
        logging.debug('request the file [%s] to url %s' % (fs_id_str, postUrl))
        data = urllib.urlencode(data)
        req = urllib2.Request(postUrl, data)
        result = json.loads(urllib2.urlopen(req).read())
        logging.debug('get the share link from baidu %s' % json.dumps(result))
        return result

    def __parseFileNameFromUserTypes__(self, receiveContent):
        return receiveContent.replace(u'搜书 ', '').strip()
