#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime

from weibo_prediction.config import events
from weibo_prediction.utils import *


def collect_mids(twfilename, lifespan):
    '''
    twfilename: 测试微博
    lifespan: 只保留（0， lifespan）期间的转发数
    '''
    mid2rtseries = {} # {mid: [[time0, uid0], [time1, uid1], ...]}

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



def predict_rtnums(tefilename, retfilename, category, uid2influence, gamma):
    '''
    tefilename: 测试微博
    retfilename: 结果文件
    category: 事件类别
    uid2influence: 用户影响力
    gamma: 时间衰减速度
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
