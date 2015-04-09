#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
from weibo_prediction.utils import *
from weibo_prediction.luo2012.config import *


def check_user_overlap(infilenames1, infilenames2):
    uids1 = set()
    uids2 = set()


    for infilename1 in infilenames1:
        with open(infilename1) as infile1:
            for line in infile1:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    uid = fields['rtUid'].split('$', 1)[0]
                else:
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                uids1.add(uid)

    for infilename2 in infilenames2:
        with open(infilename2) as infile2:
            for line in infile2:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    uid = fields['rtUid'].split('$', 1)[0]
                else:
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                uids2.add(uid)

    return len(uids1), len(uids2), len(uids1.intersection(uids2)), len(uids1.union(uids2))


if __name__ == '__main__':
    
    print 'checking user overlap...'
    infilenames1 = CHECK_USER_OVERLAP['test']
    infilenames2 = CHECK_USER_OVERLAP['top']
    len_uids1, len_uids2, len_intersection, len_union = check_user_overlap(infilenames1, infilenames2)
    print len_uids1, len_uids2, len_intersection, len_union, len_intersection / float(len_union)
