#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.config import events
from weibo_prediction.common.preprocess import extract_tweets_by_lifespans

if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime' for item in events]
    outfilenames = [infilename + '.lifespan' for infilename in infilenames]
    lifespans = [2 * 24 * 60 * 60 for _ in infilenames]
    extract_tweets_by_lifespans(infilenames, outfilenames, lifespans)
