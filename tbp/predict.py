#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
import random

from weibo_prediction.config import events
from weibo_prediction.utils import *
from weibo_prediction.influences.leaderrank import calculate_user_influences


def get_follower_uids(fsdirname, followee_uid):

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


def get_user_influences_from_fonums(trfilename, fsdirname, uid2influence):
    '''
    基于度
    '''
    with open(trfilename) as trfile:
        for line in trfile:
            fields = get_fields(line)
            if 'rtUid' in fields: # 转发微博
                uids = [_.split('$', 1)[0] for _ in fields['uid'].split('\t')]
                rtuid = fields['rtUid'].split('$', 1)[0]
                for uid in uids:
                    if uid not in uid2influence:
                        follower_uids = get_follower_uids(fsdirname, uid)
                        uid2influence[uid] = len(follower_uids)
                if rtuid not in uid2influence:
                    follower_uids = get_follower_uids(fsdirname, rtuid)
                    uid2influence[rtuid] = len(follower_uids)
            else: # 原始微博
                uid = fields['uid'].split('$', 1)[0]
                if uid not in uid2influence:
                    follower_uids = get_follower_uids(fsdirname, uid)
                    uid2influence[uid] = len(follower_uids)

    return uid2influence


def get_user_influences_from_retweets(trfilename, uid2influence):
    '''
    基于转发记录
    '''
    with open(trfilename) as trfile:
        for line in trfile:
            fields = get_fields(line)
            if 'rtUid' in fields: # 转发微博
                rtuid = fields['rtUid'].split('$', 1)[0]
                uids = [_.split('$', 1)[0] for _ in fields['uid'].split('\t')]
                uid2influence[rtuid] = uid2influence.get(rtuid, 0) + math.e ** (- len(uids))
                for i, uid in enumerate(uids[1: ]):
                    uid2influence[uid] = uid2influence.get(uid, 0) + math.e ** (- (i + 1))
            else: # 原始微博
                uid = fields['uid'].split('$', 1)[0]

    return uid2influence


def get_user_influences_from_fonums_and_retweets(uiffilename, uirfilename, alpha, uid2influence):
    '''
    基于度和转发记录
    '''
    with open(uiffilename) as uiffile:
        for line in uiffile:
            uid, influence = line.strip().split()
            uid2influence[uid] = alpha * float(influence)

    with open(uirfilename) as uirfile:
        for line in uirfile:
            uid, influence = line.strip().split()
            uid2influence[uid] = uid2influence.get(uid, 0) + (1 - alpha) * float(influence)

    return uid2influence


def get_user_influences_by_leaderrank(trfilenames, fsdirname):
 
    uids = set()

    for trfilename in trfilenames:
        with open(trfilename) as trfile:
            for line in trfile:
                fields = get_fields(line)
                if 'rtUid' in fields: # 转发微博
                    uids_ = [_.split('$', 1)[0] for _ in fields['uid'].split('\t')]
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    for uid in uids_:
                        uids.add(uid)
                    uids.add(rtuid)
                else: # 原始微博
                    uid = fields['uid'].split('$', 1)[0]
                    uids.add(uid)

    uid2influence = calculate_user_influences(fsdirname, uids)

    return uid2influence



def read_user_influences(infilename):

    uid2influence = {}

    with open(infilename) as infile:
        for line in infile:
            uid, influence = line.strip().split()
            uid2influence[uid] = float(influence)

    return uid2influence


def write_user_influences(outfilename, uid2influence):

    with open(outfilename, 'w') as outfile:
        for uid, influence in uid2influence.iteritems():
            outfile.write('%s\t%.4f\n' % (uid, influence))


def collect_mids(infilename, tiw, trw, gamma, uid2influence, mid2uid, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore):

    tiw = datetime.timedelta(seconds=tiw)
    trw = datetime.timedelta(seconds=trw)

    with open(infilename) as infile:
        for line in infile:
            fields = get_fields(line)
            if 'rtMid' in fields: # 转发微博
                rtmid = fields['rtMid']
                uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                rtuid = fields['rtUid'].split('$', 1)[0]
                time = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
                rttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
                delta = time - rttime
                if rtmid in mid2fnrtnum: # 原始微博已添加
                    mid2fnrtnum[rtmid] += 1
                    if delta <= trw:
                        mid2trrtnum[rtmid] += 1
                        if delta <= tiw:
                            mid2tirtnum[rtmid] += 1
                            #mid2tiscore[rtmid] += uid2influence.get(uid, 0) * math.e ** (- gamma * (rttime + tiw - time).seconds / 60)
                            mid2tiscore[rtmid] += math.e ** (- gamma * (rttime + tiw - time).seconds / 60)
                            #mid2tiscore[rtmid] += convert_influence(uid2influence.get(uid, 0)) * math.e ** (- gamma * (rttime + tiw - time).seconds / 60)
                else: # 原始微博未添加
                    mid2uid[rtmid] = rtuid
                    mid2fnrtnum[rtmid] = 0
                    #mid2tiscore[rtmid] = uid2influence.get(rtuid, 0) * math.e ** (- gamma * tiw.seconds / 60)
                    mid2tiscore[rtmid] = math.e ** (- gamma * tiw.seconds / 60)
                    #mid2tiscore[rtmid] = convert_influence(uid2influence.get(rtuid, 0)) * math.e ** (- gamma * tiw.seconds / 60)
                    if delta <= trw: #
                        mid2trrtnum[rtmid] = 1
                        if delta <= tiw:
                            mid2tirtnum[rtmid] = 1
                            #mid2tiscore[rtmid] += uid2influence.get(uid, 0) * math.e ** (- gamma * (rttime + tiw - time).seconds / 60)
                            mid2tiscore[rtmid] += math.e ** (- gamma * (rttime + tiw - time).seconds / 60)
                            #mid2tiscore[rtmid] += convert_influence(uid2influence.get(uid, 0)) * math.e ** (- gamma * (rttime + tiw - time).seconds / 60)
                        else:
                            mid2tirtnum[rtmid] = 0
                    else:
                        mid2trrtnum[rtmid] = 0
                        mid2tirtnum[rtmid] = 0
            else: # 原始微博
                mid = fields['mid']
                uid = fields['uid'].split('$', 1)[0]
                mid2uid[mid] = uid
                mid2fnrtnum[mid] = 0
                mid2trrtnum[mid] = 0
                mid2tirtnum[mid] = 0
                #mid2tiscore[mid] = uid2influence.get(uid, 0) * math.e ** (- gamma * tiw.seconds / 60)
                mid2tiscore[mid] = math.e ** (- gamma * tiw.seconds / 60)
                #mid2tiscore[mid] = convert_influence(uid2influence.get(uid, 0)) * math.e ** (- gamma * tiw.seconds / 60)

    return mid2uid, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore


def write_mids(outfilename, mid2uid, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore):

    with open(outfilename, 'w') as outfile:
        for mid in mid2fnrtnum:
            uid = mid2uid[mid]
            fnrtnum = mid2fnrtnum[mid]
            trrtnum = mid2trrtnum[mid]
            tirtnum = mid2tirtnum[mid]
            tiscore = mid2tiscore[mid]
            if trrtnum > 100: # 实际转发数100以上
                outfile.write('%s\t%s\t%d\t%d\t%d\t%.4f\n' % (mid, uid, fnrtnum, trrtnum, tirtnum, tiscore))


def predict_rtnums(tefilename, retfilename, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore):
    '''
    tefilename: 测试微博
    retfilename: 结果文件
    '''

    with open(retfilename, 'w') as retfile:
        for mid in mid2fnrtnum:
            trM1 = mid2trrtnum[mid]
            if trM1 > 100: # 实际转发数100以上
                print 'Start predicting M1 for %s. (time=%s)' % (mid, currenttime())
                tiM1 = mid2tirtnum[mid]
                M1 = mid2tiscore[mid]
                error = abs(M1 - trM1) / float(trM1)
                retfile.write('%s\t%.4f\t%d\t%d\t%d\n' % (mid, error, trM1, M1, tiM1))


if __name__ == '__main__':
    
    # config
    trfilenames = [event['path'] + '.eventtime.trw' for event in events if event['usage'] == 'Train'][:1]
    tefilenames = [event['path'] + '.eventtime.trw.common' for event in events if event['usage'] == 'Test']
    fsdirname = '/mnt/data2/followships/'
    retdirname = '/mnt/exps/tbp/'
    retfilenames = [os.path.join(retdirname, event['name']) for event in events if event['usage'] == 'Test']
    uilfilename = os.path.join(retdirname, 'user_influences_leaderrank')
    uiffilename = os.path.join(retdirname, 'user_influences_fonums')
    uirfilename = os.path.join(retdirname, 'user_influences_retweets')
    uifrfilename = os.path.join(retdirname, 'user_influences_fonums_and_retweets')
    midfilename = os.path.join(retdirname, 'mids')
    tiw = 60 * 60
    trw = 3 * 24 * 60 * 60
    alpha = 0.05
    gamma = 0.8

    #
    uid2influence = {}
    mid2uid = {}
    mid2fnrtnum = {}
    mid2trrtnum = {}
    mid2tirtnum = {}
    mid2tiscore = {}

    print 'Start collecting user influences....'
    #for trfilename in trfilenames:
    #    print 'Start collecting user influences from %s. (time=%s)' % (trfilename, currenttime())
    #    uid2influence = get_user_influences_from_fonums(trfilename, fsdirname, uid2influence)

    #uid2influence = get_user_influences_from_fonums_and_retweets(uiffilename, uirfilename, alpha, uid2influence)
    #uid2influence = read_user_influences(uiffilename)
    uid2influence = get_user_influences_by_leaderrank(trfilenames, fsdirname)
 
    print 'Start writing user influences...'
    write_user_influences(uilfilename, uid2influence)

    #print 'Start collecting mids...'
    #for trfilename in trfilenames:
    #    print 'Start collecting mids from %s. (time=%s)' % (trfilename, currenttime())
    #    mid2uid, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore = collect_mids(trfilename, tiw, trw, gamma, uid2influence, mid2uid, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore)

    #print 'Start writing mids...'
    #write_mids(midfilename, mid2uid, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore)

    #print 'Start predicting rtnums...'
    #for tefilename, retfilename in zip(tefilenames, retfilenames):
    #    print 'Start predicting rtnums for %s. (time=%s)' % (tefilename, currenttime())
    #    predict_rtnums(tefilename, retfilename, mid2fnrtnum, mid2trrtnum, mid2tirtnum, mid2tiscore)
