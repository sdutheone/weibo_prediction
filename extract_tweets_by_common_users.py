#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.common.preprocess import extract_tweets_by_common_users
from weibo_prediction.config import events
import sys

if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Test']
    outfilenames = [infilename + '.common' for infilename in infilenames]
    
    common_users = set()
    with open(sys.argv[1]) as infile:
        for line in infile:
            uid = line.strip()
            common_users.add(uid)

    extract_tweets_by_common_users(infilenames, outfilenames, common_users)
