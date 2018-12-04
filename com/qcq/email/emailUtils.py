#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月4日

@author: chuanqin
'''

#===============================================================================
# below original code comes from the link:https://blog.csdn.net/gpf951101/article/details/78909233
# great thanks to this great man. I modify the code to suit my own project.
# also reference for attachment of email https://github.com/rootzhongfengshan/python_practical/blob/master/SentMail/SentMailWithAttachment.py
#===============================================================================

import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from com.qcq.config.config import settings


def send_mail(recv, title, content, attachments, mail_host='smtp.163.com', port=465):
    username = settings.get(u'email section', u'email user')
    passwd = settings.get(u'email section', u'email password')
    content = '<h1>'+content+'</h1><p>WeChat Official account QCQ.</p>' 
    msg = MIMEText(content, 'html')
    
    message = MIMEMultipart()
    message['Subject'] = title
    message['From'] = username
    message['To'] = recv
    message.attach(msg)
    for fileName in attachments:
        attachment = MIMEText(open(fileName, 'rb').read(), 'base64', 'utf-8')
        attachment["Content-Type"] = 'application/octet-stream'
        attachment["Content-Disposition"] = 'attachment; filename="' + fileName + '"'
        message.attach(attachment)
    try:
        print 'Begin Connect...'
        smtp = smtplib.SMTP_SSL(mail_host, port=port)
        print 'Begin Login...'
        smtp.login(username, passwd)
        print 'Begin Send...'
        smtp.sendmail(username, recv, message.as_string())
        smtp.quit()
        print('email send success.')
    except Exception, exc:
        print exc, traceback.print_exc()
