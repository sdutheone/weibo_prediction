#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
from weibo_prediction.zhang2012.config import *

def check_overlaps(infilenames):
    filename_mids = {}

    for infilename in infilenames:
        mids = set()
        filename_mids[infilename] = mids
        with open(infilename) as infile:
            for line in infile:
                mid = line.strip().split('\t', 1)[0]
                mids.add(mid)

    for infilename1, mids1 in filename_mids.items():
        for infilename2, mids2 in filename_mids.items():
            union = mids1.union(mids2)
            intersection = mids1.intersection(mids2)
            print infilename1, infilename2, len(intersection), len(union)

    #items = filename_mids.items()
    #union = items[0][1]
    #intersection = items[0][1]
    #for i in range(1, len(items)):
    #    union = union.union(items[i][1])
    #    intersection = intersection.intersection(items[i][1])

    #return len(intersection), len(union)


if __name__ == '__main__':
    
    print 'checking overlaps...'
    print check_overlaps(CHECK_OVERLAPS['test'])
    print check_overlaps(CHECK_OVERLAPS['top'])
    print check_overlaps(CHECK_OVERLAPS['all'])
