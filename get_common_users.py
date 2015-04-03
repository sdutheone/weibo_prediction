#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.common.preprocess import get_common_users
from weibo_prediction.config import events
import sys

if __name__ == '__main__':
    infilenames1 = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Train']
    infilenames2 = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Test']
    outfilename = sys.argv[1]
    uids1, uids2, intersection = get_common_users(infilenames1, infilenames2)
    print len(uids1), len(uids2), len(intersection)
    with open(outfilename, 'w') as outfile:
        for uid in intersection:
            outfile.write(uid + '\n')
