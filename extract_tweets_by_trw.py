#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events


def extract_tweets_by_trw(infilename, outfilename, trw):
    '''
    trw: tr窗口长度
    '''
    trw = datetime.timedelta(seconds=trw)
    mid2trw = {}

    with open(infilename) as infile: # 获取微博活跃时间
        for line in infile:
            fields = get_fields(line)
            endtime = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
            if 'rtMid' in fields:
                mid = fields['rtMid']
                starttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
            else:
                mid = fields['mid']
                starttime = endtime
            mid2trw[mid] = endtime - starttime

    for mid, trw_ in mid2trw.items(): # 剔除活跃时间过短的微博
        if trw_ < trw:
            del mid2trw[mid]

    with open(infilename) as infile:
        with open(outfilename, 'w') as outfile:
            for line in infile:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    mid = fields['rtMid']
                else:
                    mid = fields['mid']
                if mid in mid2trw:
                    outfile.write(line)


def extract_tweets_by_trws(infilenames, outfilenames, trws):
    for infilename, outfilename, trw in zip(infilenames, outfilenames, trws):
        extract_tweets_by_trw(infilename, outfilename, trw)


if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime' for item in events]
    outfilenames = [infilename + '.trw' for infilename in infilenames]
    trws = [3 * 24 * 60 * 60 for _ in infilenames]
    extract_tweets_by_trws(infilenames, outfilenames, trws)
