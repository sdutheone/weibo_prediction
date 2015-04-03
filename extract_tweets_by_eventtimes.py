#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.config import events
from weibo_prediction.common.preprocess import extract_tweets_by_eventtimes

if __name__ == '__main__':
    infilenames = [item['path'] for item in events]
    outfilenames = [infilename + '.eventtime' for infilename in infilenames]
    eventtimes = [item['time'] for item in events]
    extract_tweets_by_eventtimes(infilenames, outfilenames, eventtimes)
