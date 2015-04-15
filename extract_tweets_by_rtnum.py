#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events


def extract_tweets_by_rtnum_(infilename, outfilename, rtnum):
    '''
    rtnum: 转发数
    '''
    mid_rtnums = defaultdict(int)

    with open(infilename) as infile: # 获取rtnum
        for line in infile:
            fields = get_fields(line)
            if 'rtMid' in fields:
                mid = fields['rtMid']
                mid_rtnums[mid] += 1
            else:
                mid = fields['mid']
                mid_rtnums[mid] = 0

    for mid, rtnum_ in mid_rtnums.items(): # 剔除转发数少于rtnum的微博
        if rtnum_ < rtnum:
            del mid_rtnums[mid]

    with open(infilename) as infile:
        with open(outfilename, 'w') as outfile:
            for line in infile:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    mid = fields['rtMid']
                else:
                    mid = fields['mid']
                if mid in mid_rtnums:
                    outfile.write(line)


def extract_tweets_by_rtnum(infilenames, outfilenames, rtnum):
    for infilename, outfilename in zip(infilenames, outfilenames):
        extract_tweets_by_rtnum_(infilename, outfilename, rtnum)


if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime.lifespan.common' if item['usage'] == 'Test' else item['path'] + '.eventtime.lifespan' for item in events]
    outfilenames = [infilename + '.nonzero' for infilename in infilenames]
    rtnum = 1
    extract_tweets_by_rtnum(infilenames, outfilenames, rtnum)
