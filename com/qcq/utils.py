#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018Âπ?11Êú?13Âè?

This util file is in nearing abandoned, this script used for to put the whole
project source file into one folder path to executed.
if not should add this whole project in PATH evn.

@author: chuanqin
'''

import shutil
import sys, os


def findFilesEndsWith(path, suffix):
    sourceFiles = []
    for root, directory, files in os.walk(path):
        for fileName in files:
            if fileName.upper().endswith(suffix):
                sourceFiles.append(os.path.join(os.path.abspath(root), fileName))
    return sourceFiles


def copyFilesToDst(files, dst):
    for fileName in files:
        print 'copying', fileName, 'to', path
        shutil.copy2(fileName, dst)


def countSourceCodeLine(files):
    counter = {}
    for fileName in files:
        with open(fileName, 'r') as f:
            counter[fileName] = 0
            comment = False
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if comment and line != r"'''":
                        continue
                    if not comment and line == r"'''" :
                        comment = True
                        continue
                    if comment and line == r"'''":
                        comment = False
                        continue
                    counter[fileName] += 1

    source_file_code = 0
    for file_name, line_numbers in counter.items():
        print file_name, 'contains', line_numbers, 'line codes'
        source_file_code += line_numbers
    print 'This project contains', source_file_code, 'line codes.'


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'please input where do you want to copy these files.'
        sys.exit()
    path = sys.argv[1]
    sourceFiles = findFilesEndsWith(u'.', u'PY')
    pictureFiles = findFilesEndsWith(u'.', u'JPG')
    print 'will copy the files:', sourceFiles, " to ", os.path.abspath(path)
    '''
    put the python source code to sys.argv[1] path.
    '''
    copyFilesToDst(sourceFiles, path)

    '''
    put the jpg file to sys.argv[1]/pictures path
    '''
    picturePath = os.path.join(os.path.abspath(path), 'pictures')
    if os.path.exists(picturePath):
        print picturePath, 'exist, will delete it first.'
        shutil.rmtree(picturePath, ignore_errors=True)
    os.mkdir(os.path.join(os.path.abspath(path), 'pictures'))
    print 'create folder', picturePath
    print 'will copy the files:', pictureFiles, " to ", os.path.abspath(picturePath)
    copyFilesToDst(pictureFiles, picturePath)

    countSourceCodeLine(sourceFiles)
