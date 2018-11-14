#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 2018年11月13号

@author: chuanqin
'''

import sys, os

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'please input where do you want to copy these files.'
        sys.exit()
    path = sys.argv[1]
    full_files = []
    for root, directory, files in os.walk("."):
        for fileName in files:
            if str(fileName).upper().endswith('PY'):
                full_files.append(os.path.join(os.path.abspath(root), fileName))
    print 'will copy the files:', full_files, " to ", os.path.abspath(path)

    for fileName in full_files:
        with open(fileName, 'r') as f_read:
            with open(os.path.join(path, os.path.basename(fileName)), 'w') as f_write:
                print 'will copy ', fileName, ' to ', os.path.join(path, os.path.basename(fileName))
                for line in f_read:
                    if 'com.qcq' in line:
                        line = line.split(' ')[0] + ' ' + line.split('.')[-1]
                    f_write.write(line)
            # with open(os.path.basename(fileName))
