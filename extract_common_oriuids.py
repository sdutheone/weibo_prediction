#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo_prediction.utils import *
from weibo_prediction.config import events
import sys


def extract_oriuids(infilename):
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


def extract_common_oriuids(trfilenames, tefilenames):
    truids = set()
    teuids = set()
    for trfilename in trfilenames:
        truids = truids.union(extract_oriuids(trfilename))
    for tefilename in tefilenames:
        teuids = teuids.union(extract_oriuids(tefilename))
    return truids, teuids, truids.intersection(teuids)


if __name__ == '__main__':
    trfilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Train']
    tefilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Test']
    retfilename = sys.argv[1]
    truids, teuids, intersection = extract_common_oriuids(trfilenames, tefilenames)
    print len(truids), len(teuids), len(intersection)
    with open(retfilename, 'w') as retfile:
        for uid in intersection:
            retfile.write(uid + '\n')
