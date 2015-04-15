#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
from weibo_prediction.utils import *


def write_curves(outfilename, mid_eventnames, mid_uids, mid_times, mid_rtnums, m, timeunit):
    mids = mid_rtnums.keys()
    mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)

    with open(outfilename, 'w') as outfile:
        for mid in mids:
            curve = [0]
            rttime = datetime.datetime.strptime(mid_times[mid][0], '%Y-%m-%d %H:%M:%S')
            for i in range(len(mid_times[mid]) - 1):
                time = datetime.datetime.strptime(mid_times[mid][i + 1], '%Y-%m-%d %H:%M:%S')
                delta = time - rttime
                tunums = (delta.days * 24 * 60 * 60 + delta.seconds) / timeunit + 1
                while len(curve) < tunums:
                    curve.append(0)
                curve[-1] += 1
            truncated_curve = curve[: m]
            outfile.write('%s\t' % mid)
            outfile.write('%s\t' % mid_eventnames[mid])
            outfile.write('%s\t' % mid_uids[mid])
            outfile.write('%d\t' % mid_rtnums[mid])
            outfile.write('%d\t' % sum(truncated_curve))
            outfile.write(' '.join([str(_) for _ in truncated_curve]))
            outfile.write('\n')


def collect_mids(infilename, outfilename):
    mid_eventnames = {}
    mid_uids = {}
    mid_times = {}
    mid_rtnums = {}

    with open(infilename) as infile: # 读入事件相关微博
        for line in infile:
            fields = get_fields(line)
            time = fields['time']
            if 'rtMid' in fields: # 转发微博
                rtmid = fields['rtMid']
                if rtmid in mid_rtnums: # 已添加对应的原始微博
                    mid_times[rtmid].append(time)
                    mid_rtnums[rtmid] += 1
                else: # 未添加对应的原始微博
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    rttime = fields['rtTime']
                    mid_eventnames[rtmid] = infilename.rsplit('/', 1)[-1]
                    mid_uids[rtmid] = rtuid
                    mid_times[rtmid] = [rttime, time]
                    mid_rtnums[rtmid] = 1
            else: # 原始微博
                mid = fields['mid']
                uid = fields['uid'].split('$', 1)[0]
                mid_eventnames[mid] = infilename.rsplit('/', 1)[-1]
                mid_uids[mid] = uid
                mid_times[mid] = [time]
                mid_rtnums[mid] = 0

    return mid_eventnames, mid_uids, mid_times, mid_rtnums


def get_top_n_curves_from_event(infilename, outfilename, n, m, timeunit):
    mid_eventnames, mid_uids, mid_times, mid_rtnums = collect_mids(infilename, outfilename)
    mids = mid_rtnums.keys() # 取 top n
    mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)
    if n > 0:
        for mid in mids[n: ]:
            del mid_eventnames[mid]
            del mid_uids[mid]
            del mid_times[mid]
            del mid_rtnums[mid]
    write_curves(outfilename, mid_eventnames, mid_uids, mid_times, mid_rtnums, m, timeunit)


def get_top_n_curves_from_event_group(infilenames, outfilename, n, m, timeunit):
    mid_eventnames = {}
    mid_uids = {}
    mid_times = {}
    mid_rtnums = {}

    for infilename in infilenames:
        mid_eventnames_, mid_uids_, mid_times_, mid_rtnums_ = collect_mids(infilename, outfilename)
        for mid in mid_rtnums_: # 合并
            mid_eventnames[mid] = mid_eventnames_[mid]
            mid_uids[mid] = mid_uids_[mid]
            mid_times[mid] = mid_times_[mid]
            mid_rtnums[mid] = mid_rtnums_[mid]
        mids = mid_rtnums.keys() # 取 top n
        mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)
        if n > 0:
            for mid in mids[n: ]:
                del mid_eventnames[mid]
                del mid_uids[mid]
                del mid_times[mid]
                del mid_rtnums[mid]
    
    write_curves(outfilename, mid_eventnames, mid_uids, mid_times, mid_rtnums, m, timeunit)


def calc_curve_sim(curve1, curve2):
    '''
    比较两条转发曲线相似度
    curve1: 转发曲线1
    curve2: 转发曲线2
    '''
    l = min(len(curve1), len(curve2))
    return pearson_corr(curve1[: l], curve2[: l])


def predict_rtnums(infilename1, infilename2, outfilename, simthreshold, errthreshold, m):
    '''
    预测微博转发数
    infilename1: 事件转发曲线
    infilename2: 测试微博的转发曲线
    outfilename: 结果文件
    simthreshold: 相似度阈值
    errthreshold: 误差阈值
    m: 预测所用曲线点数
    '''
    mid_topcurves = {}

    with open(infilename1) as infile1: # 读入事件类别下top n转发曲线
        for line in infile1:
            segs = line.strip().split('\t')
            mid = segs[0]
            curve = [int(_) for _ in segs[5].split()]
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
                    sim = calc_curve_sim(truncated_testcurve, topcurve)
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
                if realM1 >= 100: # 实际转发数大于0
                    error = abs(M1 - realM1) / float(realM1)
                #else:
                #    ## TODO
                #    #if M1 == 0:
                #    #    error = 0
                #    #else:
                #    #    error = float('inf')
                #    error = float('inf')
                    correct = 1 if error <= errthreshold else 0
                    outfile.write('%s\t%d\t%d\t%.4f\t%d\n' % (mid, realM1, M1, error, correct))


#def calc_precision(infilename):
#    '''
#    计算准确率
#    infilename: 预测结果文件
#    '''
#    correct = 0
#    total = 0
#
#    with open(infilename) as infile:
#        for line in infile:
#            segs = line.strip().split()
#            if segs[4] == '1':
#                correct += 1
#            total += 1
#
#    return correct, total
