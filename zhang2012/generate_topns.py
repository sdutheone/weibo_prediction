#!/usr/bin python
# -*- coding: utf-8 -*-
from weibo_prediction.config import events
from weibo_prediction.utils import *
import datetime
import os
import sys


MB = 1024 * 1024


def convert_size_to_topn(size):
    
    if size <= 1 * MB:
        return 5
    elif size <= 10 * MB:
        return 10
    elif size <= 100 * MB:
        return 20
    else:
        return 30


def generate_topns(retfilename):
    
    names = [event['name'] for event in events if event['usage'] == 'Train']
    filenames = [event['path'] + '.eventtime.trw' for event in events if event['usage'] == 'Train']
    sizes = [os.path.getsize(filename) for filename in filenames]
    topns = [convert_size_to_topn(size) for size in sizes]

    with open(retfilename, 'w') as retfile:
        for name, topn in zip(names, topns):
            retfile.write('"%s": %d,\n' % (name, topn))


if __name__ == '__main__':
    generate_topns(sys.argv[1])
