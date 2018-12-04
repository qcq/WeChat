#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年12月4日

@author: chuanqin
'''

#===============================================================================
# below original code comes from the link:https://blog.csdn.net/gpf951101/article/details/78909233
# great thanks to this great man. I modify the code to suit my own project.
#===============================================================================

import smtplib
from email.mime.text import MIMEText
from com.qcq.config import settings


def send_mail(recv, title, content, mail_host='smtp.163.com', port=465):
    username = settings.get(u'email section', u'email user')
    passwd = settings.get(u'email section', u'email password')
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = username
    msg['To'] = recv
    print 'Begin Connect...'
    smtp = smtplib.SMTP_SSL(mail_host, port=port)
    print 'Begin Login...'
    smtp.login(username, passwd)
    print 'Begin Send...'
    smtp.sendmail(username, recv, msg.as_string())
    smtp.quit()
    print('email send success.')
