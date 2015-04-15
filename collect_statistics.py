#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
from weibo_prediction.config import events
from weibo_prediction.utils import *
import os
import sys
import time


def collect_statistics(infilenames, categories, lifespan):
    
    mid2rtnum = defaultdict(int)
    mid2categorie = {}
    mid2uid = {}
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
                    deltasecs = delta.days * 24 * 60 * 60
                    if rtmid in mid2rtnum:
                        if deltasecs <= lifespan:
                            mid2rtnum[rtmid] += 1
                    else:
                        if deltasecs <= lifespan:
                            mid2rtnum[rtmid] += 1
                        else:
                            mid2rtnum[rtmid] = 0
                        mid2categorie[rtmid] = category
                else: # 原始微博
                    mid = fields['mid']
                    mid2rtnum[mid] = 0
                    mid2categorie[mid] = category

    categories_deduped = set(categories)
    for category in categories_deduped:
        category2stat[category]['tnum'] = 0
        category2stat[category]['rtnum'] = 0
    for mid, rtnum in mid2rtnum.items():
        category = mid2categorie[mid]
        category2stat[category]['tnum'] += 1
        category2stat[category]['rtnum'] += 1

    category2stat['Overall']['tnum'] = sum([stat['tnum'] for stat in category2stat.values()])
    category2stat['Overall']['rtnum'] = sum([stat['rtnum'] for stat in category2stat.values() if 'rtnum' in stat])

    for category, stat in category2stat.items():
        print '%s\t\t\t%d\t\t%d' % (category, stat['tnum'], stat['rtnum'])


if __name__ == '__main__':
    trfilenames = [item['path'] for item in events if item['usage'] == 'Train']
    tefilenames = [item['path'] for item in events if item['usage'] == 'Test']
    trcategories = [item['category'] for item in events if item['usage'] == 'Train']
    tecategories = [item['category'] for item in events if item['usage'] == 'Test']
    lifespan = 2 * 24 * 60 * 60

    print 'Train tweets'
    collect_statistics(trfilenames, trcategories, lifespan)
    print 'Test tweets'
    collect_statistics(tefilenames, tecategories, lifespan)
