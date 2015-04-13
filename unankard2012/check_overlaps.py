#!/usr/bin python
# -*- coding: utf-8 -*-
from weibo_prediction.config import events, unankard2012
from weibo_prediction.utils import *
import sys


def check_user_overlap(infilenames1, infilenames2, outfilename1, outfilename2):
    '''
    infilenames1: 训练微博
    infilenames2: 测试微博
    outfilename1: 训练微博中出现的uid
    outfilename2: 测试微博中出现的uid
    '''
    uids1 = set()
    uids2 = set()

    for infilename1 in infilenames1:
        print 'collecting uids from', infilename1
        with open(infilename1) as infile1:
            for line in infile1:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    uids = [_.split('$', 1)[0] for _ in fields['uid'].split('\t')]
                    uids1.add(rtuid)
                    uids1.update(uids)
                else:
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                    uids1.add(uid)

    for infilename2 in infilenames2:
        print 'collecting uids from', infilename2
        with open(infilename2) as infile2:
            for line in infile2:
                fields = get_fields(line)
                if 'rtMid' in fields:
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    uids = [_.split('$', 1)[0] for _ in fields['uid'].split('\t')]
                    uids2.add(rtuid)
                    uids2.update(uids)
                else:
                    uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
                    uids2.add(uid)

    with open(outfilename1, 'w') as outfile1:
        for uid in uids1:
            outfile1.write('%s\n' % uid)

    with open(outfilename2, 'w') as outfile2:
        for uid in uids2:
            outfile2.write('%s\n' % uid)

    return len(uids1), len(uids2), len(uids1.intersection(uids2)), len(uids1.union(uids2))


if __name__ == '__main__':
    infilenames1 = [item['path'] for item in events if item['usage'] == 'Train']
    infilenames2 = [item['path'] for item in events if item['usage'] == 'Test']
    outfilename1 = sys.argv[1]
    outfilename2 = sys.argv[2]
    len_uids1, len_uids2, len_intersection, len_union = check_user_overlap(infilenames1, infilenames2, outfilename1, outfilename2)
    print len_uids1, len_uids2, len_intersection, len_union, len_intersection / float(len_union)
