#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
import random
import sys
import compago
from collections import defaultdict
from weibo_prediction.utils import *


app = compago.Application()


@app.option('-i', dest='infilename')
@app.option('-o', dest='outdirname')
def extract_tweets_by_events(infilename, outdirname):
    '''
    抽取存在对应事件的原始微博及其转发微博
    '''
    mid_eventnames = {}
    eventname_files = {}

    with open(infilename) as infile:
        for line in infile:
            fields = get_fields(line)
            eventname = ''
            if 'eventList' in fields:
                eventname = fields['eventList'].split('\t', 1)[0].split('$', 1)[0]
            elif 'rtEventList' in fields:
                eventname = fields['rtEventList'].split('\t', 1)[0].split('$', 1)[0]
            if eventname:
                if eventname not in eventname_files:
                    eventname_files[eventname] = open(os.path.join(outdirname, eventname), 'w')
                eventname_files[eventname].write(line)

if __name__ == '__main__':
    app.run()
