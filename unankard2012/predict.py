#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import networkx as nx

from weibo_prediction.config import events
from weibo_prediction.utils import *


def get_tweet_frequencies(trfilenames, categories):

    Ts = {}
    RTs = {}

    for trfilename, category in zip(trfilenames, categories):
        with open(trfilename) as trfile:
            for line in trfile:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                    if rtuid not in RTs:
                        RTs[rtuid] = {}
                    if uid not in RTs[rtuid]:
                        RTs[rtuid][uid] = {}
                    RTs[rtuid][uid][category] = RTs[rtuid][uid].get(category, 0) + 1
                else:
                    uid = fields['uid'].split('$', 1)[0]
                    if uid not in Ts:
                        Ts[uid] = {}
                    Ts[uid][category] = Ts[uid].get(category, 0) + 1

    return Ts, RTs


def get_follower_uids(fsdirname, uid):
    '''
    fsdirname: 用户关系文件所在目录
    uid: 用户uid
    '''
    follower_uids = set()
    
    with open(os.path.join(fsdirname, uid)) as fsfile:
        for line in fsfile:
            follower_uid, followee_uid = line.strip().split()
            follower_uids.add(follower_uid)
    
    return follower_uids


#def collect_mids(twfilename, lifespan):
#    '''
#    twfilename: 测试微博
#    lifespan: 只保留lifespan期间的转发者
#    '''
#    mid_uids = {}
#    mid_retweeters = {} # 包括发布者
#    mid_rtnums = {}
#
#    with open(twfilename) as twfile:
#        for line in twfile:
#            fields = get_fields(line)
#            if 'rtMid' in fields:
#                rtmid = fields['rtMid']
#                rtuid = fields['rtUid'].split('$', 1)[0]
#                uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
#                time = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
#                rttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
#                delta = time - rttime
#                if rtmid in mid_rtnums:
#                    if delta.days * 24 * 60 * 60 + delta.seconds <= lifespan: #
#                        mid_retweeters[rtmid].append(uid)
#                        mid_rtnums[rtmid] += 1
#                else:
#                    mid_uids[rtmid] = rtuid
#                    if delta.days * 24 * 60 * 60 + delta.seconds <= lifespan: #
#                        mid_retweeters[rtmid] = [rtuid, uid]
#                        mid_rtnums[rtmid] = 1
#                    else:
#                        mid_retweeters[rtmid] = [rtuid]
#                        mid_rtnums[rtmid] = 0
#            else:
#                mid = fields['mid']
#                uid = fields['uid'].split('$', 1)[0]
#                mid_uids[mid] = uid
#                mid_retweeters[mid] = [uid]
#                mid_rtnums[mid] = 0
#
#    return mid_uids, mid_retweeters, mid_rtnums


def collect_mids(twfilename, lifespan):
    '''
    twfilename: 测试微博
    lifespan: 只保留lifespan期间的转发者
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
                if rtmid in mid_rtnums:
                    if delta.days * 24 * 60 * 60 + delta.seconds <= lifespan: #
                        mid_retweeters[rtmid].append(uid)
                        mid_rtnums[rtmid] += 1
                else:
                    if delta.days * 24 * 60 * 60 + delta.seconds <= lifespan: #
                        mid_retweeters[rtmid] = [rtuid, uid]
                        mid_rtnums[rtmid] = 1
                    else:
                        mid_retweeters[rtmid] = [rtuid]
                        mid_rtnums[rtmid] = 0
            else:
                mid = fields['mid']
                uid = fields['uid'].split('$', 1)[0]
                mid_retweeters[mid] = [uid]
                mid_rtnums[mid] = 0

    return mid_retweeters, mid_rtnums


#def predict_rtnums(infilename, indirname, category, Ts, RTs, lambda_):
#    '''
#    infilename: 测试微博
#    indirname: 用户网络
#    category: 类别
#    Ts: ###
#    RTs: ###
#    lambda_: 转发阈值
#    '''
#    print 'Collect mids...'
#    mid_uids, mid_retweeters, mid_rtnums = collect_mids(infilename, 2*60*60)
#    processed_uids = set()
#
#    for mid in mid_uids:
#        M1 = len(mid_retweeters[mid]) - 1
#        uid = mid_uids[mid]
#        print 'Get network...'
#        network = get_network(indirname, uid)
#        retweeters = mid_retweeters[mid]
#        while len(retweeters) > 0:
#            retweeter = retweeters.pop()
#            for follower in network.successors_iter(retweeter):
#                if follower in RTs[retweeter] and category in RTs[retweeter][follower]:
#                    RT = RTs[retweeter][follower][category] # TODO
#                else:
#                    RT = 0
#                if category in Ts[uid]:
#                    T = Ts[uid][category]
#                    P = RT / float(T)
#                else:
#                    P = 0
#                if P >= lambda_:
#                    if follower not in processed_uids:
#                        M1 += 1
#                        processed_uids.add(follower)
#
#        realM1 = mid_rtnums[mid]
#        if realM1 >= 100: # 转发数100以上
#            print M1, realM1
#            error = abs(M1 - realM1) / float(realM1)
#            outfile.write('%s\t%d\t%d\t%.4f\n' % (mid, realM1, M1, error))


def predict_rtnums(tefilename, fsdirname, category, Ts, RTs, lambda_):
    '''
    tefilename: 测试微博
    fsdirname: 用户关系文件所在目录
    category: 事件类别
    Ts: ###
    RTs: ###
    lambda_: 转发阈值
    '''
    print 'Collect mids...'
    mid_retweeters, mid_rtnums = collect_mids(tefilename, 2*60*60)
    uids_to_process = set()
    #uids_processed = set()

    for mid, retweeter_uids in retweeters.iteritems():
        realM1 = mid_rtnums[mid]
        if realM1 >= 100: # 实际转发数100以上
            M1 = len(retweeter_uids) - 1
            uid = retweeter_uids[0]
            uids_to_process = uids_to_process.union(retweeter_uids)
            while len(uids_to_process) > 0:
                retweeter_uid = uids_to_process.pop()
                for follower_uid in get_follower_uids(fsdirname, retweeter_uid):
                    if follower_uid in RTs[retweeter_uid] and category in RTs[retweeter_uid][follower_uid]:
                        RT = RTs[retweeter_uid][follower_uid][category]
                    else:
                        RT = 0
                    if category in Ts[uid]:
                        T = Ts[uid][category]
                        P = RT / float(T)
                    else:
                        P = 0
                    if P >= lambda_: # 转发
                        uids_to_process.add(follower_uid)
                        #if follower not in processed_uids:
                        M1 += 1
                        #processed_uids.add(follower)
            print M1, realM1
            error = abs(M1 - realM1) / float(realM1)
            outfile.write('%s\t%d\t%d\t%.4f\n' % (mid, realM1, M1, error))



if __name__ == '__main__':
    
    # config
    trfilenames = [item['path'] for item in events if item['usage'] == 'Train']
    tefilenames = [item['path'] for item in events if item['usage'] == 'Test']
    fsdirname = '/mnt/data2/followships/'
    trcategories = [item['category'] for item in events if item['usage'] == 'Train']
    tecategories = [item['category'] for item in events if item['usage'] == 'Test']
    lambda_ = 0.6

    print 'Get tweet frequencies...'
    Ts, RTs = get_tweet_frequencies(trfilenames, trcategories)
    Ts, RTs = {}, {}

    print 'Predict rtnums...'
    for tefilename, tecategory in zip(tefilenames, tecategories):
        print 'Predict rtnums for', tefilename
        predict_rtnums(tefilename, fsdirname, tecategory, Ts, RTs, lambda_)
