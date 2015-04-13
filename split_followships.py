#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.config import events
from weibo_prediction.utils import *
import os
import sys


def split_followships(fsfilename, retdirname):
    '''
    fsfilename: 用户关系
    retdirname: 结果目录
    '''
    retfiles = {}

    with open(fsfilename) as fsfile:
        for line in fsfile:
            follower_uid, followee_uid = line.strip().split()
            if followee_uid in retfiles:
                retfile = retfiles[followee_uid]
            else:
                if len(retfiles) >= 500:
                    for uid in retfiles.keys():
                        retfiles[uid].close()
                    retfiles = {}
                retfile = open(os.path.join(retdirname, followee_uid), 'a')
                retfiles[followee_uid] = retfile
            retfile.write(line)


if __name__ == '__main__':
    fsfilename = sys.argv[1]
    retdirname = sys.argv[2]
    split_followships(fsfilename, retdirname)
