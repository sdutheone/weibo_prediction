#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
from weibo_prediction.config import events, zhang2012
from weibo_prediction.zhang2012.predict import *


if __name__ == '__main__':
    categories = set()
    for event in events:
        categories.add(event['category'])

    #print 'get top n curves...'
    #for category in categories:
    #    infilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['category'] == category and item['usage'] == 'Train']
    #    outdirname = zhang2012['outdirname']
    #    outfilename = os.path.join(outdirname, '%s.curves' % category)
    #    timeunit = zhang2012['timeunit']
    #    m = zhang2012['m']
    #    n = zhang2012['n']
    #    print 'get top n curves from %s...' % category
    #    get_top_n_curves_from_event_group(infilenames, outfilename, n, m, timeunit)

    print 'get test curves...'
    for category in categories:
        infilenames = [item['path'] + '.eventtime.lifespan.common' for item in events if item['category'] == category and item['usage'] == 'Test']
        outdirname = zhang2012['outdirname']
        outfilename = os.path.join(outdirname, category + '.test.curves')
        timeunit = zhang2012['timeunit']
        m = zhang2012['m']
        n = -1
        print 'get curves form %s...' % ', '.join([infilename.rsplit('/', 1)[-1] for infilename in infilenames])
        get_top_n_curves_from_event_group(infilenames, outfilename, n, m, timeunit)


    #print 'predict rtnums...'
    #indirname = zhang2012['outdirname']
    #infilenames1 = [os.path.join(indirname, category + '.curves') for category in categories]
    #infilenames2 = [os.path.join(indirname, category + '.test.curves') for category in categories]
    #outfilenames = [os.path.join(indirname, category + '.results') for category in categories]
    #pm = zhang2012['pm']
    #simthreshold = zhang2012['simthreshold']
    #errthreshold = zhang2012['errthreshold']
    #for infilename1, infilename2, outfilename in zip(infilenames1, infilenames2, outfilenames):
    #    print 'predict rtnums for %s...' % infilename2
    #    predict_rtnums(infilename1, infilename2, outfilename, simthreshold, errthreshold, pm)

    #print 'calculate precision...'
    #correct_overall = 0
    #total_overall = 0
    #precisions = {}

    #indirname = zhang2012['outdirname']
    #infilenames = [os.path.join(indirname, category + '.results') for category in categories]
    #for infilename in infilenames:
    #    correct, total = calc_precision(infilename)
    #    precisions[infilename.rsplit('/', 1)[-1]] = correct, total
    #    correct_overall += correct
    #    total_overall += total
    #for eventname, (correct, total) in precisions.items():
    #    if total == 0:
    #        print eventname, correct, total, 0.0
    #    else:
    #        print eventname, correct, total, float(correct) / total
    #print 'overall', correct_overall, total_overall, float(correct_overall) / total_overall
