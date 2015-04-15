#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
import random

from weibo_prediction.config import events
from weibo_prediction.utils import *


def get_tweet_frequencies(trfilenames, categories):

    Ts = {}
    RTs = {}
    processed_mids = set()

    for trfilename, category in zip(trfilenames, categories):
        with open(trfilename) as trfile:
            for line in trfile:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    rtmid = fields['rtMid']
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                    if rtuid not in Ts:
                        Ts[rtuid] = {}
                    if rtmid not in processed_mids:
                        Ts[rtuid][category] = Ts[rtuid].get(category, 0) + 1
                        processed_mids.add(rtmid)
                    if rtuid not in RTs:
                        RTs[rtuid] = {}
                    if uid not in RTs[rtuid]:
                        RTs[rtuid][uid] = {}
                    RTs[rtuid][uid][category] = RTs[rtuid][uid].get(category, 0) + 1
                else:
                    mid = fields['mid']
                    uid = fields['uid'].split('$', 1)[0]
                    if uid not in Ts:
                        Ts[uid] = {}
                    Ts[uid][category] = Ts[uid].get(category, 0) + 1
                    processed_mids.add(mid)

    return Ts, RTs


def get_follower_uids(fsdirname, followee_uid):
    '''
    fsdirname: 用户关系文件所在目录
    uid: 用户uid
    '''
    fsfilename = fsdirname
    for s in followee_uid[-4: ]:
        fsfilename = os.path.join(fsfilename, s)
    fsfilename = os.path.join(fsfilename, followee_uid + '.fs')

    follower_uids = set()
    if os.path.exists(fsfilename):
        with open(fsfilename) as fsfile:
            for line in fsfile:
                follower_uid = line.strip()
                follower_uids.add(follower_uid)
    
    return follower_uids


def collect_mids(twfilename, lifespan, plifespan):
    '''
    twfilename: 测试微博
    lifespan: 只保留（0， lifespan）期间的转发数
    plifespan: 只保留（0， plifespan）期间的转发用户
    '''
    mid_retweeters = {} # 包括发布者
    mid_rtnums = {}

    with open(twfilename) as twfile:
        for line in twfile:
            fields = get_fields(line)
            if 'rtMid' in fields:
                rtmid = fields['rtMid']
                rtuid = fields['rtUid'].split('$', 1)[0]
                uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                time = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
                rttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
                delta = time - rttime
                deltasecs = delta.days * 24 * 60 * 60 + delta.seconds
                if rtmid in mid_rtnums:
                    if deltasecs <= lifespan: #
                        mid_rtnums[rtmid] += 1
                        if deltasecs <= plifespan:
                            mid_retweeters[rtmid].append(uid)
                else:
                    if deltasecs <= lifespan: #
                        mid_rtnums[rtmid] = 1
                        mid_retweeters[rtmid] = [rtuid]
                        if deltasecs <= plifespan:
                            mid_retweeters[rtmid].append(uid)
                    else:
                        mid_retweeters[rtmid] = [rtuid]
                        mid_rtnums[rtmid] = 0
            else:
                mid = fields['mid']
                uid = fields['uid'].split('$', 1)[0]
                mid_retweeters[mid] = [uid]
                mid_rtnums[mid] = 0

    return mid_retweeters, mid_rtnums


def predict_rtnums(tefilename, fsdirname, retfilename, category, Ts, RTs, lambda_):
    '''
    tefilename: 测试微博
    fsdirname: 用户关系文件所在目录
    retfilename: 结果文件
    category: 事件类别
    Ts: ###
    RTs: ###
    lambda_: 转发阈值
    '''
    print 'Start collecting mids. (time=%s)' % currenttime()
    mid_retweeters, mid_rtnums = collect_mids(tefilename, 2*24*60*60, 2*60*60)
    uids_to_process = set()
    uids_processed = set()

    with open(retfilename, 'w') as retfile:
        for mid, retweeter_uids in mid_retweeters.iteritems():
            realM1 = mid_rtnums[mid]
            if realM1 >= 100: # 实际转发数100以上
                print 'Start predicting M1 for %s. (time=%s)' % (mid, currenttime())
                M1 = len(retweeter_uids) - 1
                uid = retweeter_uids[0]
                uids_to_process = uids_to_process.union(retweeter_uids)
                while len(uids_to_process) > 0:
                    #print len(uids_to_process)
                    retweeter_uid = uids_to_process.pop()
                    for follower_uid in get_follower_uids(fsdirname, retweeter_uid):
                        if uid in RTs and follower_uid in RTs[uid] and\
                                category in RTs[uid][follower_uid]:
                            RT = RTs[uid][follower_uid][category]
                        else:
                            RT = 0
                        if uid in Ts and category in Ts[uid]:
                            T = Ts[uid][category]
                            P = RT / float(T)
                        else:
                            T = 0
                            P = 0
                        if P > 0:
                            print uid, follower_uid, RT, T, P
                        if P > lambda_ and follower_uid not in uids_processed: # 转发
                            uids_to_process.add(follower_uid)
                            M1 += 1
                    uids_processed.add(retweeter_uid)
                error = abs(M1 - realM1) / float(realM1)
                retfile.write('%s\t%d\t%d\t%.4f\t%d\n' % (mid, realM1, M1, error, len(retweeter_uids) - 1))


if __name__ == '__main__':
    
    # config
    trfilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Train']
    tefilenames = [item['path'] + '.eventtime.lifespan.common' for item in events if item['usage'] == 'Test']
    fsdirname = '/mnt/data2/followships/'
    retdirname = '/mnt/exps/unankard2012/'
    retfilenames = [os.path.join(retdirname, item['name']) for item in events if item['usage'] == 'Test']
    trcategories = [item['category'] for item in events if item['usage'] == 'Train']
    tecategories = [item['category'] for item in events if item['usage'] == 'Test']
    lambda_ = 0.05

    print 'Get tweet frequencies...'
    Ts, RTs = get_tweet_frequencies(trfilenames, trcategories)
    #Ts, RTs = {}, {}

    print 'Predict rtnums...'
    for tefilename, retfilename, tecategory in zip(tefilenames, retfilenames, tecategories):
        print 'Predict rtnums for', tefilename
        predict_rtnums(tefilename, fsdirname, retfilename, tecategory, Ts, RTs, lambda_)
