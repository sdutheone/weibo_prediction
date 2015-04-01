#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
from weibo_prediction.utils import *
from weibo_prediction.zhang2012.config import *


def zhang2012_select_top_n_tweets(infilenames, eventtimes, unittime, m, n, outfilename):
    '''
    infilenames: 事件微博文件
    eventtimes: 事件发生时间，格式'yyyy-mm-dd HH:MM:SS'
    unittime: 单位时间(秒)
    m: 曲线点数
    n: 选取数量, n小于等于0则全部选取
    outfilename: 结果文件
    '''
    mid_eventnames = {}
    mid_times = {}
    mid_rtnums = {}
    
    for infilename, eventtime in zip(infilenames, eventtimes):
        zhang2012_collect_tweets(infilename, eventtime, unittime, m, n, mid_eventnames, mid_times, mid_rtnums)
    zhang2012_write_curves(mid_eventnames, mid_times, mid_rtnums, m, outfilename)


def zhang2012_calc_curve_sim(curve1, curve2):
    '''
    比较两条转发曲线相似度
    curve1: 转发曲线1
    curve2: 转发曲线2
    '''
    l = min(len(curve1), len(curve2))
    return pearson_corr(curve1[: l], curve2[: l])


def zhang2012_collect_tweets(infilename, eventtime, unittime, m, n, mid_eventnames, mid_times, mid_rtnums):
    '''
    统计微博数据
    infilename: 事件微博文件
    eventtime: 事件发生时间，格式'yyyy-mm-dd HH:MM:SS'
    unittime: 单位时间(秒)
    m: 曲线最少点数
    n: 选取转发最多的top n，若n小于等于0，则全选
    outfilename: 结果文件
    '''
    # 读入事件相关微博
    with open(infilename) as infile:
        for line in infile:
            fields = get_fields(line)
            time = fields['time']
            if 'rtMid' in fields: # 转发微博
                rtmid = fields['rtMid']
                rttime = fields['rtTime']
                if rtmid in mid_rtnums: # 已添加对应的原始微博
                    mid_times[rtmid].append(time)
                    mid_rtnums[rtmid] += 1
                elif rttime >= eventtime: # 未添加对应的原始微博，且原始微博在事件发生后发布
                    mid_eventnames[rtmid] = infilename.rsplit('/', 1)[-1]
                    mid_times[rtmid] = [rttime]
                    mid_rtnums[rtmid] = 1
            else: # 原始微博
                mid = fields['mid']
                if time >= eventtime: # 在事件发生后发布
                    mid_eventnames[mid] = infilename.rsplit('/', 1)[-1]
                    mid_times[mid] = [time]
                    mid_rtnums[mid] = 0

    # 只保留时间跨度超过指定长度的微博
    lifespan = datetime.timedelta(seconds=unittime*m)
    mids = mid_rtnums.keys()
    for mid in mids:
        rttime = datetime.datetime.strptime(mid_times[mid][0], '%Y-%m-%d %H:%M:%S')
        time = datetime.datetime.strptime(mid_times[mid][-1], '%Y-%m-%d %H:%M:%S')
        delta = time - rttime
        if delta < lifespan:
            del mid_eventnames[mid]
            del mid_times[mid]
            del mid_rtnums[mid]

    # 取top n
    mids = mid_rtnums.keys()
    mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)
    if n > 0:
        for mid in mids[n: ]:
            del mid_eventnames[mid]
            del mid_times[mid]
            del mid_rtnums[mid]


def zhang2012_write_curves(mid_eventnames, mid_times, mid_rtnums, m, outfilename):
    '''
    保存转发曲线
    mid_eventnames: 事件名称
    mid_times: 转发时间
    mid_rtnums: 转发数
    m: 曲线点数
    outfilename: 结果文件
    '''
    mids = mid_rtnums.keys()
    mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)

    with open(outfilename, 'w') as outfile:
        for mid in mids:
            curve = [0]
            rttime = datetime.datetime.strptime(mid_times[mid][0], '%Y-%m-%d %H:%M:%S')
            for i in range(len(mid_times[mid]) - 1):
                time = datetime.datetime.strptime(mid_times[mid][i + 1], '%Y-%m-%d %H:%M:%S')
                delta = time - rttime
                utnums = (delta.days * 24 * 3600 + delta.seconds) / unittime + 1
                while len(curve) < utnums:
                    curve.append(0)
                curve[-1] += 1
            #while len(curve) < m: # 点数小于n，扩展
            #    curve.append(0)
            truncated_curve = curve[: m]
            outfile.write('%s\t' % mid)
            outfile.write('%s\t' % mid_eventnames[mid])
            outfile.write('%d\t' % mid_rtnums[mid])
            outfile.write('%d\t' % sum(truncated_curve))
            outfile.write(' '.join([str(_) for _ in truncated_curve]))
            outfile.write('\n')


def zhang2012_get_test_curves(infilename, eventtime, unittime, m, outfilename):
    '''
    生成测试微博的转发曲线
    infilename: 测试微博文件
    eventtime: 事件发生时间，格式'yyyy-mm-dd HH:MM:SS'
    unittime: 单位时间(秒)
    m: 曲线点数
    outfilename: 结果文件
    '''
    mid_eventnames = {}
    mid_times = {}
    mid_rtnums = {}
    zhang2012_collect_tweets(infilename, eventtime, unittime, m, 0, mid_eventnames, mid_times, mid_rtnums)
    zhang2012_write_curves(mid_eventnames, mid_times, mid_rtnums, m, outfilename)


def zhang2012_predict_rtnums(infilename1, infilename2, simthreshold, errthreshold, m, outfilename):
    '''
    预测微博转发数
    infilename1: 事件转发曲线
    infilename2: 测试微博的转发曲线
    simthreshold: 相似度阈值
    errthreshold: 误差阈值
    m: 预测所用曲线点数
    outfilename: 结果文件
    '''
    mid_topcurves = {}

    with open(infilename1) as infile1: # 读入事件类别下top n转发曲线
        for line in infile1:
            segs = line.strip().split('\t')
            mid = segs[0]
            curve = [int(_) for _ in segs[4].split()]
            mid_topcurves[mid] = curve

    with open(outfilename, 'w') as outfile: # 预测并保存结果
        with open(infilename2) as infile2:
            for line in infile2:
                segs = line.strip().split('\t')
                mid = segs[0]
                testcurve = [int(_) for _ in segs[4].split()]
                truncated_testcurve = testcurve[: m]
                candidates = []
                for topcurve in mid_topcurves.itervalues():
                    sim = zhang2012_calc_curve_sim(truncated_testcurve, topcurve)
                    if sim >= simthreshold:
                        candidates.append(topcurve)
                M1 = 0
                M1s = []
                realM1 = sum(testcurve)
                error = 0
                correct = 0
                for candidate in candidates:
                    s = 0
                    zipped_curves = zip(truncated_testcurve, topcurve)
                    len_zipped = len(zipped_curves)
                    for point1, point2 in zipped_curves:
                        if point2 != 0:
                            s += point1 / float(point2)
                    ratio = s / len_zipped
                    M1s.append(int(ratio * sum(topcurve)))
                if len(candidates) > 0: # 存在候选微博
                    M1 = int(sum(M1s) / float(len(M1s)))
                else:
                    M1 = sum(truncated_testcurve)
                if realM1 > 0: # 实际转发数大于0
                    error = abs(M1 - realM1) / float(realM1)
                else:
                    error = float('inf')
                correct = 1 if error <= errthreshold else 0
                outfile.write('%s\t%d\t%d\t%.4f\t%d\n' % (mid, realM1, M1, error, correct))


def zhang2012_calc_precision(infilename):
    '''
    计算准确率
    infilename: 预测结果文件
    '''
    correct = 0
    total = 0

    with open(infilename) as infile:
        for line in infile:
            segs = line.strip().split()
            if segs[4] == '1':
                correct += 1
            total += 1

    return correct, total



if __name__ == '__main__':
    #print 'selecting top n tweets...'
    #for category in SELECT_TOP_N_TWEETS_CONFIGS:
    #    infilenames = SELECT_TOP_N_TWEETS_CONFIGS[category]['infilenames']
    #    eventtimes = SELECT_TOP_N_TWEETS_CONFIGS[category]['eventtimes']
    #    unittime = SELECT_TOP_N_TWEETS_CONFIGS[category]['unittime']
    #    m = SELECT_TOP_N_TWEETS_CONFIGS[category]['m']
    #    n = SELECT_TOP_N_TWEETS_CONFIGS[category]['n']
    #    outfilename = SELECT_TOP_N_TWEETS_CONFIGS[category]['outfilename']
    #    print 'selecting top n tweets from %s...' % category
    #    zhang2012_select_top_n_tweets(infilenames, eventtimes, unittime, m, n, outfilename)

    #print 'generating testcurves...'
    #for config in GET_TEST_CURVES_CONFIGS:
    #    infilename = config['infilename']
    #    eventtime = config['eventtime']
    #    unittime = config['unittime']
    #    m = config['m']
    #    outfilename = config['outfilename']
    #    print 'generating testcurves for %s...' % infilename.rsplit('/', 1)[-1]
    #    zhang2012_get_test_curves(infilename, eventtime, unittime, m, outfilename)

    print 'predicting rtnums...'
    for config in PREDICT_RTNUMS_CONFIGS:
        infilename1 = config['infilename1']
        infilename2 = config['infilename2']
        simthreshold = config['simthreshold']
        errthreshold = config['errthreshold']
        m = config['m']
        outfilename = config['outfilename']
        print 'predicting rtnums for %s...' % infilename2
        zhang2012_predict_rtnums(infilename1, infilename2, simthreshold, errthreshold, m, outfilename)

    print 'calculating precision...'
    correct_overall = 0
    total_overall = 0
    precisions = {}
    for infilename in CALC_PRECISION['infilenames']:
        print 'calculating precision for %s...' % infilename
        correct, total = zhang2012_calc_precision(infilename)
        precisions[infilename.rsplit('/', 1)[-1]] = correct, total
        correct_overall += correct
        total_overall += total
    for eventname, (correct, total) in precisions.items():
        print eventname, correct, total, float(correct) / total
    print 'overall', correct_overall, total_overall, float(correct_overall) / total_overall
