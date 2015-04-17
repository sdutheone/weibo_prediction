#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os

from weibo_prediction.config import events
from weibo_prediction.utils import *


def collect_mids(tefilename, tiw, trw):
    '''
    tefilename: 测试微博
    tiw: ti窗口长度
    trw: tr窗口长度
    '''
    tiw = datetime.timedelta(seconds=tiw)
    trw = datetime.timedelta(seconds=trw)
    mid2tirtnum = {}
    mid2trrtnum = {}

    with open(tefilename) as tefile:
        for line in tefile:
            fields = get_fields(line)
            if 'rtMid' in fields:
                rtmid = fields['rtMid']
                time = datetime.datetime.strptime(fields['time'], '%Y-%m-%d %H:%M:%S')
                rttime = datetime.datetime.strptime(fields['rtTime'], '%Y-%m-%d %H:%M:%S')
                delta = time - rttime
                if rtmid in mid2tirtnum: # 已添加
                    if delta <= trw:
                        mid2trrtnum[rtmid] += 1
                        if delta <= tiw:
                            mid2tirtnum[rtmid] += 1
                else: # 未添加
                    if delta <= trw: #
                        mid2trrtnum[rtmid] = 1
                        if delta <= tiw:
                            mid2tirtnum[rtmid] = 1
                        else:
                            mid2tirtnum[rtmid] = 0
                    else:
                        mid2trrtnum[rtmid] = 0
            else:
                mid = fields['mid']
                mid2tirtnum[mid] = 0
                mid2trrtnum[mid] = 0

    return mid2tirtnum, mid2trrtnum


def predict_rtnums(tefilename, retfilename, category, mid2tirtnum, mid2trrtnum):
    '''
    tefilename: 测试微博
    retfilename: 结果文件
    category: 事件类别
    mid2tirtnum: #
    mid2trrtnum: #
    '''

    with open(retfilename, 'w') as retfile:
        for mid in mid2tirtnum:
            M1 = mid2tirtnum[mid]
            realM1 = mid2trrtnum[mid]
            if realM1 > 100:
                error = abs(M1 - realM1) / float(realM1)
                retfile.write('%s\t%.4f\t%d\t%d\t%d\n' % (mid, error, realM1, M1, M1))


if __name__ == '__main__':
    
    # config
    tefilenames = [item['path'] + '.eventtime.trw.common' for item in events if item['usage'] == 'Test']
    retdirname = '/mnt/exps/baseline/'
    retfilenames = [os.path.join(retdirname, item['name']) for item in events if item['usage'] == 'Test']
    tecategories = [item['category'] for item in events if item['usage'] == 'Test']
    tiw = 1 * 60 * 60
    trw = 3 * 24 * 60 *60

    for tefilename, retfilename, tecategory in zip(tefilenames, retfilenames, tecategories):
        print 'Start collecting mids. (time=%s)' % currenttime()
        mid2tirtnum, mid2trrtnum = collect_mids(tefilename, tiw, trw)
        print 'Start predicting rtnums for', tefilename
        predict_rtnums(tefilename, retfilename, tecategory, mid2tirtnum, mid2trrtnum)
