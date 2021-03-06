#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月4日

@author: chuanqin
'''

#=========================================================================
# below original code comes from the link:https://blog.csdn.net/gpf951101/article/details/78909233
# great thanks to this great man. I modify the code to suit my own project.
# also reference for attachment of email
# https://github.com/rootzhongfengshan/python_practical/blob/master/SentMail/SentMailWithAttachment.py
# also write one blog of own->https://blog.csdn.net/u011233383/article/details/84794295
#=========================================================================

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import smtplib
import traceback

from com.qcq.config.config import settings
from com.qcq.const.message import email_default_signature


def send_mail(recv, title, content, attachments, mail_host = 'smtp.163.com', port = 465):
    username = settings.get(u'email section', u'email user')
    passwd = settings.get(u'email section', u'email password')
    content = '<h1>' + content + '</h1><p>' + email_default_signature + '.</p>'
    msg = MIMEText(content, 'html')

    message = MIMEMultipart()
    message['Subject'] = title
    message['From'] = username
    message['To'] = recv
    message.attach(msg)
    for fileName in attachments:
        attachment = MIMEText(open(fileName, 'rb').read(), 'base64', 'utf-8')
        attachment["Content-Type"] = 'application/octet-stream'
        attachment["Content-Disposition"] = 'attachment; filename="' + \
            fileName + '"'
        message.attach(attachment)
    try:
        logging.info('Begin Connect...')
        smtp = smtplib.SMTP_SSL(mail_host, port = port)
        logging.info('Begin Login... %s' % (username))
        smtp.login(username, passwd)
        logging.info('Begin Send... to %s' % (':'.join(recv)))
        smtp.sendmail(username, recv, message.as_string())
        smtp.quit()
        logging.info('email send success.')
    except Exception, exc:
        logging.warn('Exception happened:%s' %
            traceback.print_exc(), exc_info = True)
