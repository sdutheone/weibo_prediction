#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events
import sys


def get_users(infilename):
    uids = set()
    with open(infilename) as infile:
        for line in infile:
            fields = get_fields(line)
            if 'rtUid' in fields:
                uid = fields['rtUid'].split('$', 1)[0]
            else:
                uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
            uids.add(uid)
    return uids


def get_common_users(infilenames1, infilenames2):
    uids1 = set()
    uids2 = set()
    for infilename1 in infilenames1:
        uids1 = uids1.union(get_users(infilename1))
    for infilename2 in infilenames2:
        uids2 = uids2.union(get_users(infilename2))
    return uids1, uids2, uids1.intersection(uids2)


if __name__ == '__main__':
    infilenames1 = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Train']
    infilenames2 = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Test']
    outfilename = sys.argv[1]
    uids1, uids2, intersection = get_common_users(infilenames1, infilenames2)
    print len(uids1), len(uids2), len(intersection)
    with open(outfilename, 'w') as outfile:
        for uid in intersection:
            outfile.write(uid + '\n')
