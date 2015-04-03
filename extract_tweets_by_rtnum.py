#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.config import events
from weibo_prediction.common.preprocess import extract_tweets_by_rtnum

if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime.lifespan.common' if item['usage'] == 'Test' else item['path'] + '.eventtime.lifespan' for item in events]
    outfilenames = [infilename + '.nonzero' for infilename in infilenames]
    rtnum = 1
    extract_tweets_by_rtnum(infilenames, outfilenames, rtnum)
