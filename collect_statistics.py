#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from weibo_prediction.config import events
from weibo_prediction.utils import *
import os
import sys
import time


def collect_statistics(infilenames, categories, tiw, trw):
   
    tiw = datetime.timedelta(seconds=tiw)
    trw = datetime.timedelta(seconds=trw)

    mid2uid = {}
    mid2category = {}
    mid2tirtnum = {}
    mid2trrtnum = {}
    mid2fnrtnum = {}

    category2stat = defaultdict(dict)
 
    for infilename, category in zip(infilenames, categories):
        with open(infilename) as infile:
            for line in infile:
                fields = get_fields(line)
                if 'rtMid' in fields: # 转发微博
                    rtmid = fields['rtMid']
                    rttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
                    time = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
                    delta = time - rttime
                    if rtmid in mid2fnrtnum: # 已添加
                        mid2fnrtnum[rtmid] += 1
                        if delta <= trw:
                            mid2trrtnum[rtmid] += 1
                            if delta <= tiw:
                                mid2tirtnum[rtmid] += 1
                    else: # 未添加
                        rtuid = fields['rtUid'].split('$', 1)[0]
                        mid2uid[rtmid] = rtuid
                        mid2category[rtmid] = category
                        mid2fnrtnum[rtmid] = 1
                        if delta <= trw:
                            mid2trrtnum[rtmid] = 1
                            if delta <= tiw:
                                mid2tirtnum[rtmid] = 1
                            else:
                                mid2tirtnum[rtmid] = 0
                        else:
                            mid2trrtnum[rtmid] = 0
                            mid2tirtnum[rtmid] = 0
                else: # 原始微博
                    mid = fields['mid']
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                    mid2uid[mid] = uid
                    mid2category[mid] = category
                    mid2fnrtnum[mid] = 0
                    mid2tirtnum[mid] = 0
                    mid2trrtnum[mid] = 0

    categories_deduped = set(categories)
    for category in categories_deduped:
        category2stat[category]['tnum'] = len([mid for mid in mid2fnrtnum if mid2category[mid] == category])
        category2stat[category]['rtnum'] = sum([mid2fnrtnum[mid] for mid in mid2fnrtnum if mid2category[mid] == category])
        category2stat[category]['uidnum'] = len(set([mid2uid[mid] for mid in mid2category if mid2category[mid] == category]))

    overallstat = {}
    overallstat['tnum'] = sum([stat['tnum'] for stat in category2stat.values()])
    overallstat['rtnum'] = sum([stat['rtnum'] for stat in category2stat.values()])
    overallstat['uidnum'] = len(set(mid2uid.values()))

    for category, stat in category2stat.items():
        print '%s\t%d\t%d\t%d\n' % (category, stat['tnum'], stat['rtnum'], stat['uidnum'])
    print 'Overall\t%d\t%d\t%d\n' % (overallstat['tnum'], overallstat['rtnum'], overallstat['uidnum'])


if __name__ == '__main__':
    trfilenames = [event['path'] + '.eventtime.trw' for event in events if event['usage'] == 'Train']
    tefilenames = [event['path'] + '.eventtime.trw.common' for event in events if event['usage'] == 'Test']
    trcategories = [event['category'] for event in events if event['usage'] == 'Train']
    tecategories = [event['category'] for event in events if event['usage'] == 'Test']
    trw = 3 * 24 * 60 * 60
    tiw = 1 * 60 * 60

    print 'Train tweets'
    collect_statistics(trfilenames, trcategories, trw, tiw)
    print 'Test tweets'
    collect_statistics(tefilenames, tecategories, trw, tiw)
