#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events


def extract_tweets_by_lifespan(infilename, outfilename, lifespan):
    '''
    lifespan: 存在时间(秒)
    '''
    lifespan = datetime.timedelta(seconds=lifespan)
    mid_lifespans = {}

    with open(infilename) as infile: # 获取lifespan
        for line in infile:
            fields = get_fields(line)
            endtime = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
            if 'rtMid' in fields:
                mid = fields['rtMid']
                starttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
            else:
                mid = fields['mid']
                starttime = endtime
            mid_lifespans[mid] = endtime - starttime

    for mid, lifespan_ in mid_lifespans.items(): # 剔除lifespan过短的微博
        if lifespan_ < lifespan:
            del mid_lifespans[mid]

    with open(infilename) as infile:
        with open(outfilename, 'w') as outfile:
            for line in infile:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    mid = fields['rtMid']
                else:
                    mid = fields['mid']
                if mid in mid_lifespans:
                    outfile.write(line)


def extract_tweets_by_lifespans(infilenames, outfilenames, lifespans):
    for infilename, outfilename, lifespan in zip(infilenames, outfilenames, lifespans):
        extract_tweets_by_lifespan(infilename, outfilename, lifespan)


if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime' for item in events]
    outfilenames = [infilename + '.lifespan' for infilename in infilenames]
    lifespans = [2 * 24 * 60 * 60 for _ in infilenames]
    extract_tweets_by_lifespans(infilenames, outfilenames, lifespans)
