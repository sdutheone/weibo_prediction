#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
import random

from weibo_prediction.config import events, luo2012
from weibo_prediction.utils import *
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import _arma_predict_out_of_sample


def write_curves(outfilename, mid_uids, mid_times, mid_rtnums, m, timeunit):
    
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
            outfile.write('%s\t' % mid_uids[mid])
            outfile.write('%d\t' % mid_rtnums[mid])
            outfile.write('%d\t' % sum(truncated_curve))
            outfile.write(' '.join([str(_) for _ in truncated_curve]))
            outfile.write('\n')


def write_curves_by_uids(outdirname, mid_uids, mid_times, mid_rtnums, m, timeunit):

    outfiles = {}
    mids = mid_rtnums.keys()
    mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)

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

        uid = mid_uids[mid]
        name = uid[-4: ]
        if name in outfiles:
            outfile = outfiles[name]
        else:
            try:
                outfile = open(os.path.join(outdirname, name), 'a')
            except IOError:
                for key in random.sample(outfiles.keys(), 500):
                    outfiles[key].close()
                    del outfiles[key]
                outfile = open(os.path.join(outdirname, name), 'a')
            finally:
                outfiles[name] = outfile
        outfile.write('%s\t' % mid)
        outfile.write('%s\t' % mid_uids[mid])
        outfile.write('%d\t' % mid_rtnums[mid])
        outfile.write('%d\t' % sum(truncated_curve))
        outfile.write(' '.join([str(_) for _ in truncated_curve]))
        outfile.write('\n')

#def write_curves_by_uids(outdirname, mid_uids, mid_times, mid_rtnums, m, timeunit):
#
#    outfiles = {}
#
#    numstrs = [str(_) for _ in range(10)]
#    names = [i + j + k + l for i in numstrs for j in numstrs for k in numstrs for l in numstrs]
#    for name in names:
#        outfiles[name] = open(os.path.join(outdirname, name), 'w')
#
#    mids = mid_rtnums.keys()
#    mids.sort(key=lambda mid: mid_rtnums[mid], reverse=True)
#
#    for mid in mids:
#        curve = [0]
#        rttime = datetime.datetime.strptime(mid_times[mid][0], '%Y-%m-%d %H:%M:%S')
#        for i in range(len(mid_times[mid]) - 1):
#            time = datetime.datetime.strptime(mid_times[mid][i + 1], '%Y-%m-%d %H:%M:%S')
#            delta = time - rttime
#            tunums = (delta.days * 24 * 60 * 60 + delta.seconds) / timeunit + 1
#            while len(curve) < tunums:
#                curve.append(0)
#            curve[-1] += 1
#        truncated_curve = curve[: m]
#
#        uid = mid_uids[mid]
#        outfile = outfiles[uid[-3: ]]
#        outfile.write('%s\t' % mid)
#        outfile.write('%s\t' % mid_uids[mid])
#        outfile.write('%d\t' % mid_rtnums[mid])
#        outfile.write('%d\t' % sum(truncated_curve))
#        outfile.write(' '.join([str(_) for _ in truncated_curve]))
#        outfile.write('\n')


def collect_mids(infilename):
    mid_uids = {}
    mid_times = {}
    mid_rtnums = {}

    with open(infilename) as infile: # 读入事件相关微博
        for line in infile:
            fields = get_fields(line)
            time = fields['time']
            uid = fields['uid'].split('\t', 1)[0].split('$', 1)[0]
            if 'rtMid' in fields: # 转发微博
                rtuid = fields['rtUid'].split('$', 1)[0]
                rtmid = fields['rtMid']
                rttime = fields['rtTime']
                if rtmid in mid_rtnums: # 已添加对应的原始微博
                    mid_times[rtmid].append(time)
                    mid_rtnums[rtmid] += 1
                else: # 未添加对应的原始微博
                    mid_uids[rtmid] = rtuid
                    mid_times[rtmid] = [rttime, time]
                    mid_rtnums[rtmid] = 1
            else: # 原始微博
                mid = fields['mid']
                mid_uids[mid] = uid
                mid_times[mid] = [time]
                mid_rtnums[mid] = 0

    return mid_uids, mid_times, mid_rtnums


def get_curves(infilename, outfilename, m, timeunit):
    '''
    生成转发曲线
    '''
    mid_uids, mid_times, mid_rtnums = collect_mids(infilename)
    write_curves(outfilename, mid_uids, mid_times, mid_rtnums, m, timeunit)


def get_curves_by_uids(infilenames, outdirname, m, timeunit):
    '''
    生成转发曲线，并按发布者uid的末尾4位数字分开保存
    '''
    mid_uids = {}
    mid_times = {}
    mid_rtnums = {}

    for infilename in infilenames:
        mid_uids_, mid_times_, mid_rtnums_ = collect_mids(infilename)
        for mid in mid_rtnums_: # 合并
            mid_uids[mid] = mid_uids_[mid]
            mid_times[mid] = mid_times_[mid]
            mid_rtnums[mid] = mid_rtnums_[mid]
    
    write_curves_by_uids(outdirname, mid_uids, mid_times, mid_rtnums, m, timeunit)


def convert_curve(curve, interval):
    n = len(curve) / interval
    cnvrt_curve = [0] * n
    for i in range(n):
        #cnvrt_curve[i] = sum(curve[: (i + 1) * interval]) # t时刻转发数
        cnvrt_curve[i] = sum(curve[i * interval: (i + 1) * interval]) # (t-1,t)期间转发数
    return cnvrt_curve


def calc_curve_sim(curve1, curve2):
    s = 0.0
    for p1, p2 in zip(curve1, curve2):
        s += (p1 - p2) ** 2
    return s


def arma_predict(candidate, curve):
    print acf(candidate)
    print pacf(candidate)
    res = sm.tsa.stattools.arma_order_select_ic(candidate, ic='aic')
    arma_mod = sm.tsa.ARMA(candidate, order=res.aic_min_order)
    arma_res = arma_mod.fit(trend='c', disp=-1)
    params = arma_res.params
    residuals = arma_res.resid
    p = arma_res.k_ar
    q = arma_res.k_ma
    k_exog = arma_res.k_exog
    k_trend = arma_res.k_trend
    steps = len(candidate) - len(curve)

    #res = sm.tsa.stattools.arma_order_select_ic(candidate, ic='aic')
    #train_mod = sm.tsa.ARMA(candidate, order=res.aic_min_order)
    #train_res = train_mod.fit(trend='c', disp=-1)
    #test_mod = sm.tsa.ARMA(curve, order=res.aic_min_order)
    #test_mod.predict(train_res, len(curve), len(candidate))

    return int(sum(curve) + sum(_arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=curve, exog=None, start=len(curve))))


def predict_rtnums(infilename, indirname, outfilename, simthreshold, errthreshold, pm, s):
    '''
    预测微博转发数
    infilename: 测试微博转发曲线文件
    indirname: 训练微博转发曲线文件所在文件夹
    outfilename: 结果文件
    simthreshold: 相似度阈值
    errthreshold: 误差阈值
    pm: 预测所用曲线点数
    s: 模型参数
    '''
    interval = pm / s

    with open(outfilename, 'w') as outfile: # 预测并保存结果
        with open(infilename) as infile1:
            for line1 in infile1:
                segs1 = line1.strip().split('\t')
                mid1 = segs1[0]
                uid1 = segs1[1]
                testcurve = [int(_) for _ in segs1[4].split()]
                trunc_testcurve = testcurve[: pm]
                cnvrt_testcurve = convert_curve(testcurve, interval) # 转换
                cnvrt_trunc_testcurve = convert_curve(trunc_testcurve, interval) # 转换
                # 找到最相似的训练微博
                sim_max = 0.0
                n = 0
                with open(os.path.join(indirname, uid1[-4: ])) as infile2:
                    for line2 in infile2:
                        segs2 = line2.strip().split('\t')
                        uid2 = segs2[1]
                        if uid1 == uid2:
                            n += 1
                            traincurve = [int(_) for _ in segs2[4].split()]
                            cnvrt_traincurve = convert_curve(traincurve, interval)
                            sim = calc_curve_sim(cnvrt_trunc_testcurve, cnvrt_traincurve) # 计算相似度
                            if sim > sim_max:
                                sim_max = sim
                                candidate = cnvrt_traincurve
                realM1 = sum(testcurve)
                if realM1 >= 100: # 实际转发数大于0
                    if sum(candidate) == 0:
                        M1 = sum(trunc_testcurve)
                        is_valid = 0
                    else:
                        try:
                            M1 =  arma_predict(candidate, cnvrt_trunc_testcurve)# TODO
                            is_valid = 1
                        except ValueError as e:
                            print e.message
                            print candidate
                            M1 = sum(trunc_testcurve)
                            is_valid = 0
                    print M1, realM1
                    error = abs(M1 - realM1) / float(realM1)
                    correct = 1 if error <= errthreshold else 0
                    outfile.write('%s\t%d\t%d\t%.4f\t%d\n' % (mid1, realM1, M1, error, is_valid))


def calc_precision(infilename):
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
    categories = set()
    for event in events:
        categories.add(event['category'])

    #print 'Generating train curves...'
    #infilenames = [item['path'] + '.eventtime.lifespan' for item in events if item['usage'] == 'Train']
    #outdirname = luo2012['outdirname']
    #timeunit = luo2012['timeunit']
    #m = luo2012['m']
    #get_curves_by_uids(infilenames, outdirname, m, timeunit)

    #print 'Generating test curves...'
    #infilenames = [item['path'] + '.eventtime.lifespan.common' for item in events if item['usage'] == 'Test']
    #outdirname = luo2012['outdirname']
    #outfilenames = [os.path.join(outdirname, infilename.rsplit('/', 1)[-1].split('.', 1)[0]) for infilename in infilenames]
    #timeunit = luo2012['timeunit']
    #m = luo2012['m']
    #for infilename, outfilename in zip(infilenames, outfilenames):
    #    print infilename, outfilename
    #    get_curves(infilename, outfilename, m, timeunit)

    print 'Predicting rtnums...'
    dirname = luo2012['outdirname']
    infilenames = [os.path.join(dirname, item['name']) for item in events if item['usage'] == 'Test']
    outfilenames = [infilename + '.results' for infilename in infilenames]
    simthreshold = luo2012['simthreshold']
    errthreshold = luo2012['errthreshold']
    timeunit = luo2012['timeunit']
    pm = luo2012['pm']
    s = luo2012['s']
    for infilename, outfilename in zip(infilenames, outfilenames):
        predict_rtnums(infilename, dirname, outfilename, simthreshold, errthreshold, pm, s)
