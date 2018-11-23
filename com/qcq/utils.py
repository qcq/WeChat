#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13号

This util file is in nearing abandoned, this script used for to put the whole
project source file into one folder path to executed.
if not should add this whole project in PATH evn.

@author: chuanqin
'''

import shutil
import sys, os

def countSourceCodeLine(files):
    counter = {}
    for file in files:
        with open(file, 'r') as f:
            counter[file] = 0
            comment = False
            for line in f:
                line = line.strip()
                if line != '':
                    if comment and line != r"'''":
                        continue
                    if not comment and line == r"'''" :
                        comment = True
                        continue
                    if comment and line == r"'''":
                        comment = False
                        continue
                    counter[file] += 1
    
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
    sourceFiles = []
    pictureFiles = []
    for root, directory, files in os.walk("."):
        for fileName in files:
            if str(fileName).upper().endswith('PY'):
                sourceFiles.append(os.path.join(os.path.abspath(root), fileName))
            if str(fileName).upper().endswith('JPG'):
                pictureFiles.append(os.path.join(os.path.abspath(root), fileName))
    print 'will copy the files:', sourceFiles, " to ", os.path.abspath(path)
    '''
    put the python source code to sys.argv[1] path.
    '''
    for fileName in sourceFiles:
        print 'copying', fileName, 'to', path
        shutil.copy2(fileName, path)

    '''
    put the jpg file to sys.argv[1]/pictures path
    '''
    picture_path = os.path.join(os.path.abspath(path), 'pictures')
    if os.path.exists(picture_path):
        print picture_path, 'exist, will delete it first.'
        shutil.rmtree(picture_path, ignore_errors=True)
    os.mkdir(os.path.join(os.path.abspath(path), 'pictures'))
    print 'create folder', picture_path
    print 'will copy the files:', pictureFiles, " to ", os.path.abspath(picture_path)
    for fileName in pictureFiles:
        print 'copying', fileName, 'to', path
        shutil.copy2(fileName, picture_path)
    
    countSourceCodeLine(sourceFiles)
