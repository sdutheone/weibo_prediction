#!/usr/bin python
# -*- coding: utf-8 -*-
from weibo_prediction.luo2012.config import *
from weibo_prediction.utils import *
import datetime
import os
import sys
import user


def stat_tweet_num(indirname):
    mids = set()

    for name in os.listdir(indirname):
        infilename = os.path.join(indirname, name)
        if os.path.isfile(infilename):
            with open(infilename) as infile:
                for line in infile:
                    fields = get_fields(line)
                    if 'rtMid' in fields:
                        mid = fields['rtMid']
                    else:
                        mid = fields['mid']
                    mids.add(mid)

    return len(mids)


if __name__ == '__main__': 
    print stat_tweet_num(sys.argv[1])
