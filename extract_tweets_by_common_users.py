#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events
import sys


def extract_tweets_by_common_users_(infilename, outfilename, common_users):
    with open(infilename) as infile:
        with open(outfilename, 'w') as outfile:
            for line in infile:
                fields = get_fields(line)
                if 'rtUid' in fields:
                    uid = fields['rtUid'].split('$', 1)[0]
                else:
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                if uid in common_users:
                    outfile.write(line)


def extract_tweets_by_common_users(infilenames, outfilenames, common_users):
    for infilename, outfilename in zip(infilenames, outfilenames):
        extract_tweets_by_common_users_(infilename, outfilename, common_users)


if __name__ == '__main__':
    infilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Test']
    outfilenames = [infilename + '.common' for infilename in infilenames]
    
    common_users = set()
    with open(sys.argv[1]) as infile:
        for line in infile:
            uid = line.strip()
            common_users.add(uid)

    extract_tweets_by_common_users(infilenames, outfilenames, common_users)
