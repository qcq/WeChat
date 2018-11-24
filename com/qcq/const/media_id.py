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

picturesPath = os.path.dirname(sys.argv[0]) + '../pictures/'

picturesData = []
for picture in utils.findFilesEndsWith(picturesPath, 'JPG'):
    temp = {}
    name = os.path.basename(picture).split('.')[0]
    temp['name'] = name
    temp['path'] = picture
    temp['media_id'] = ''
    picturesData.append(temp)


def getPictureByName(name):
    for item in picturesData:
        if item['name'] == name:
            return item
