#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events


def extract_tweets_by_eventtime(infilename, outfilename, eventtime):
    '''
    eventtime: 事件发生时间,'YY-mm-dd HH:MM:SS'
    '''
    with open(infilename) as infile:
        with open(outfilename, 'w') as outfile:
            for line in infile:
                fields = get_fields(line)
                if 'rtTime' in fields:
                    time = fields['rtTime']
                else:
                    time = fields['time']
                if time >= eventtime:
                    outfile.write(line)


def extract_tweets_by_eventtimes(infilenames, outfilenames, eventtimes):
    for infilename, outfilename, eventtime in zip(infilenames, outfilenames, eventtimes):
        extract_tweets_by_eventtime(infilename, outfilename, eventtime)


if __name__ == '__main__':
    infilenames = [item['path'] for item in events]
    outfilenames = [infilename + '.eventtime' for infilename in infilenames]
    eventtimes = [item['time'] for item in events]
    extract_tweets_by_eventtimes(infilenames, outfilenames, eventtimes)
