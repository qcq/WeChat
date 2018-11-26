#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on Nov 14, 2018

@author: qinchuanqing
'''
import os
import sys
import com.qcq.utils as utils

media_id_me = u"2Ntgs-VZxFZehdkabkeyGFmFwPMC6CHlEhdAUmhAb6HBvEhAfE3XciSBdwDZEDUh"
media_id_married = u"M3kQ9RnD7x-R3V49IG8PXwbDgIAznrXiyaKoZUV00DnJ-x_E6w-geYiyDhc26fAv"
married_image_path = r"./pictures/married.jpg"

picturesPath = u"%s%s" % (os.path.dirname(sys.argv[0]), u'../pictures/')

picturesData = []
for picture in utils.findFilesEndsWith(picturesPath, u'JPG'):
    temp = {}
    name = os.path.basename(picture).split('.')[0]
    temp[u'name'] = name
    temp[u'path'] = picture
    temp[u'media_id'] = u''
    picturesData.append(temp)


def getPictureByName(name):
    for item in picturesData:
        if item['name'] == name:
            return item
