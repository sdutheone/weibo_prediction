#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from weibo_prediction.config import events
from weibo_prediction.utils import *
import os
import sys
import time


#def split_followships(fsfilename, retdirname):
#    '''
#    fsfilename: 用户关系
#    retdirname: 结果目录
#    '''
#    retfiles = {}
#
#    with open(fsfilename) as fsfile:
#        for line in fsfile:
#            follower_uid, followee_uid = line.strip().split()
#            if followee_uid in retfiles:
#                retfile = retfiles[followee_uid]
#            else:
#                if len(retfiles) >= 500:
#                    for uid in retfiles.keys():
#                        retfiles[uid].close()
#                    retfiles = {}
#                retfile = open(os.path.join(retdirname, followee_uid), 'a')
#                retfiles[followee_uid] = retfile
#            retfile.write(line)


#def split_followships(fsfilename, retdirname):
#    '''
#    fsfilename: 用户关系
#    retdirname: 结果目录
#    '''
#    with open(fsfilename) as fsfile:
#        for line in fsfile:
#            follower_uid, followee_uid = line.strip().split()
#            retfilename = retdirname
#            for s in followee_uid[: 5]:
#                retfilename = os.path.join(retfilename, s)
#            if not os.path.exists(retfilename):
#                os.makedirs(retfilename)
#            retfilename = os.path.join(retfilename, followee_uid + '.fs')
#            retfile = open(retfilename, 'a')
#            retfile.write('%s\n' % follower_uid)
#            retfile.close()


def split_followships(fsfilename, retdirname):
    '''
    fsfilename: 用户关系
    retdirname: 结果目录
    '''
    numstrs = [str(_) for _ in range(10)]
    tags = [i + j for i in numstrs for j in numstrs]
    tags = tags[39: ]

    for tag in tags: 
        print 'Processing tag started.(tag=%s, time=%s)' % (tag, currenttime())
        feuid_fouids = defaultdict(list)
        print 'Collecting uids started.(time=%s)' % currenttime()
        with open(fsfilename) as fsfile:
            for line in fsfile:
                follower_uid, followee_uid = line.strip().split()
                if followee_uid[-2: ] == tag:
                    feuid_fouids[followee_uid].append(follower_uid)
        print 'Collecting uids finished.(time=%s)' % currenttime()
        print 'Writing uids started.(time=%s)' % currenttime()
        ntotalwrite = 0
        for followee_uid, follower_uids in feuid_fouids.iteritems():
            retfilename = retdirname
            retfilename = os.path.join(retfilename, *followee_uid[-4: ])
            if not os.path.exists(retfilename):
                os.makedirs(retfilename)
            retfilename = os.path.join(retfilename, followee_uid + '.fs')
            with open(retfilename, 'w') as retfile:
                nwrite = 0
                for follower_uid in follower_uids:
                    nwrite += 1
                    ntotalwrite += 1
                    retfile.write('%s\n' % follower_uid)
            print '%d records written.(followeeuid=%s, time=%s)' % (nwrite, followee_uid, currenttime())
        print 'Writing uids finished.(ntotalwrite=%d, time=%s)' % (ntotalwrite, currenttime())
        print 'Processing tag finished.(tag=%s, time=%s)' % (tag, currenttime())


if __name__ == '__main__':
    fsfilename = sys.argv[1]
    retdirname = sys.argv[2]
    split_followships(fsfilename, retdirname)
