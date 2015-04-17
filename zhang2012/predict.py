#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os
from weibo_prediction.config import events
from weibo_prediction.utils import *


def write_curves(outfilename, mid2eventname, mid2uid, mid2times, mid2rtnum, m, timeunit):
    mids = mid2rtnum.keys()
    mids.sort(key=lambda mid: mid2rtnum[mid], reverse=True)

    with open(outfilename, 'w') as outfile:
        for mid in mids:
            curve = [0]
            rttime = datetime.datetime.strptime(mid2times[mid][0], '%Y-%m-%d %H:%M:%S')
            for i in range(len(mid2times[mid]) - 1):
                time = datetime.datetime.strptime(mid2times[mid][i + 1], '%Y-%m-%d %H:%M:%S')
                delta = time - rttime
                tunums = (delta.days * 24 * 60 * 60 + delta.seconds) / timeunit + 1
                while len(curve) < tunums:
                    curve.append(0)
                curve[-1] += 1
            truncated_curve = curve[: m]
            outfile.write('%s\t' % mid)
            outfile.write('%s\t' % mid2eventname[mid])
            outfile.write('%s\t' % mid2uid[mid])
            outfile.write('%d\t' % mid2rtnum[mid])
            outfile.write('%d\t' % sum(truncated_curve))
            outfile.write(' '.join([str(_) for _ in truncated_curve]))
            outfile.write('\n')


def collect_mids(infilename):
    mid2eventname = {}
    mid2uid = {}
    mid2times = {}
    mid2rtnum = {}

    with open(infilename) as infile: # 读入事件相关微博
        for line in infile:
            fields = get_fields(line)
            time = fields['time']
            if 'rtMid' in fields: # 转发微博
                rtmid = fields['rtMid']
                if rtmid in mid2rtnum: # 已添加对应的原始微博
                    mid2times[rtmid].append(time)
                    mid2rtnum[rtmid] += 1
                else: # 未添加对应的原始微博
                    rtuid = fields['rtUid'].split('$', 1)[0]
                    rttime = fields['rtTime']
                    mid2eventname[rtmid] = infilename.rsplit('/', 1)[-1]
                    mid2uid[rtmid] = rtuid
                    mid2times[rtmid] = [rttime, time]
                    mid2rtnum[rtmid] = 1
            else: # 原始微博
                mid = fields['mid']
                uid = fields['uid'].split('$', 1)[0]
                mid2eventname[mid] = infilename.rsplit('/', 1)[-1]
                mid2uid[mid] = uid
                mid2times[mid] = [time]
                mid2rtnum[mid] = 0

    return mid2eventname, mid2uid, mid2times, mid2rtnum

### 每个category取topn
#def get_top_n_curves_from_event(infilename, outfilename, n, m, timeunit):
#    mid2eventname, mid2uid, mid2times, mid2rtnum = collect_mids(infilename, outfilename)
#    mids = mid2rtnum.keys() # 取 top n
#    mids.sort(key=lambda mid: mid2rtnum[mid], reverse=True)
#    if n > 0:
#        for mid in mids[n: ]:
#            del mid2eventname[mid]
#            del mid2uid[mid]
#            del mid2times[mid]
#            del mid2rtnum[mid]
#    write_curves(outfilename, mid2eventname, mid2uid, mid2times, mid2rtnum, m, timeunit)
#
#
#def get_top_n_curves_from_event_group(infilenames, outfilename, n, m, timeunit):
#    mid2eventname = {}
#    mid2uid = {}
#    mid2times = {}
#    mid2rtnum = {}
#
#    for infilename in infilenames:
#        mid2eventname_, mid2uid_, mid2times_, mid2rtnum_ = collect_mids(infilename, outfilename)
#        for mid in mid2rtnum_: # 合并
#            mid2eventname[mid] = mid2eventname_[mid]
#            mid2uid[mid] = mid2uid_[mid]
#            mid2times[mid] = mid2times_[mid]
#            mid2rtnum[mid] = mid2rtnum_[mid]
#        mids = mid2rtnum.keys() # 取 top n
#        mids.sort(key=lambda mid: mid2rtnum[mid], reverse=True)
#        if n > 0:
#            for mid in mids[n: ]:
#                del mid2eventname[mid]
#                del mid2uid[mid]
#                del mid2times[mid]
#                del mid2rtnum[mid]
#    
#    write_curves(outfilename, mid2eventname, mid2uid, mid2times, mid2rtnum, m, timeunit)



### 每个event取topn
def get_top_n_curves_from_event(infilename, n):
    mid2eventname, mid2uid, mid2times, mid2rtnum = collect_mids(infilename)
    mids = mid2rtnum.keys() # 取 top n
    mids.sort(key=lambda mid: mid2rtnum[mid], reverse=True)
    if n > 0:
        for mid in mids[n: ]:
            del mid2eventname[mid]
            del mid2uid[mid]
            del mid2times[mid]
            del mid2rtnum[mid]
    return mid2eventname, mid2uid, mid2times, mid2rtnum


def get_top_n_curves_from_event_group(infilenames, outfilename, ns, m, timeunit):
    mid2eventname = {}
    mid2uid = {}
    mid2times = {}
    mid2rtnum = {}

    for infilename, n in zip(infilenames, ns):
        mid2eventname_, mid2uid_, mid2times_, mid2rtnum_ = get_top_n_curves_from_event(infilename, n)
        for mid in mid2rtnum_: # 合并
            mid2eventname[mid] = mid2eventname_[mid]
            mid2uid[mid] = mid2uid_[mid]
            mid2times[mid] = mid2times_[mid]
            mid2rtnum[mid] = mid2rtnum_[mid]
    
    write_curves(outfilename, mid2eventname, mid2uid, mid2times, mid2rtnum, m, timeunit)


def calc_curve_sim(curve1, curve2):
    '''
    比较两条转发曲线相似度
    curve1: 转发曲线1
    curve2: 转发曲线2
    '''
    l = min(len(curve1), len(curve2))
    return pearson_corr(curve1[: l], curve2[: l])
    #return spearmanr(curve1[: l], curve2[: l])[0]


def predict_rtnums(infilename1, infilename2, outfilename, simthreshold, m):
    '''
    预测微博转发数
    infilename1: 事件转发曲线
    infilename2: 测试微博的转发曲线
    outfilename: 结果文件
    simthreshold: 相似度阈值
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
                testcurve = [int(_) for _ in segs[5].split()]
                realM1 = sum(testcurve)
                if realM1 > 100:
                    truncated_testcurve = testcurve[: m]
                    candidates = []
                    for topcurve in mid_topcurves.itervalues():
                        sim = calc_curve_sim(truncated_testcurve, topcurve)
                        if sim >= simthreshold:
                            candidates.append(topcurve)
                    M1s = []
                    tirtnum = sum(truncated_testcurve)
                    error = 0
                    for candidate in candidates:
                        s = 0
                        zipped_curves = zip(truncated_testcurve, candidate)
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
                    error = abs(M1 - realM1) / float(realM1)
                    outfile.write('%s\t%.4f\t%d\t%d\t%d\n' % (mid, error, realM1, M1, tirtnum))


if __name__ == '__main__':
    name2topn = {
        "Anshun incident": 10,
        "Bohai bay oil spill": 5,
        "case of running fast car in Heibei University": 20,
        "Chaozhou riot": 5,
        "China Petro chemical Co. Ltd": 20,
        "Chongqing gang trials": 20,
        "death of Muammar Gaddafi": 20,
        "death of Steve Jobs": 5,
        "Deng Yujiao incident": 10,
        "earthquake of Yunnan Yingjiang": 20,
        "family violence of Li Yang": 10,
        "Foxconn worker falls to death": 10,
        "Fuzhou bombings": 5,
        "Guo Meimei": 20,
        "House prices": 30,
        "incident of self-burning at Yancheng, Jangsu": 20,
        "Japan Earthquake": 5,
        "Li Na win French Open in tennis": 5,
        "line 10 of Shanghai-Metro pileup": 10,
        "mass suicide at Nanchang Bridge": 5,
        "Motorola was acquisitions by Google": 5,
        "protests of Wukan": 5,
        "Qian Yunhui": 20,
        "Qianxi riot": 5,
        "Shanghai government's urban management officers attack migrant workers in 2011": 5,
        "Shanxi": 5,
        "Shenzhou-8 launch successfully": 5,
        "Spain Series A League": 5,
        "Tang Jun educatioin qualification fake": 20,
        "the death of Osama Bin Laden": 20,
        "Tiangong-1 launch successfully": 10,
        "Wenzhou train collision": 20,
        "Windows Phone release": 20,
        "Xiaomi release": 5,
        "Yao Jiaxin murder case": 5,
        "Yihuang self-immolation incident": 10,
        "Yushu earthquake": 20,
        "Zhili disobey tax official violent": 5,
        "Zhouqu landslide": 10,
    }
    retdirname = '/mnt/exps/zhang2012'
    timeunit = 60
    m = 3 * 24 * 60 * 60 / timeunit
    pm = 60 * 60 / timeunit
    simthreshold = 0.2

    categories = set()
    for event in events:
        categories.add(event['category'])

    #print 'get top n curves...'
    #for category in categories:
    #    trnames = [event['name'] for event in events if event['category'] == category and event['usage'] == 'Train']
    #    trns = [name2topn[name] for name in trnames]
    #    print trns
    #    trfilenames = [event['path'] + '.eventtime.trw' for event in events if event['category'] == category and event['usage'] == 'Train']
    #    retfilename = os.path.join(retdirname, '%s.curves' % category)
    #    print 'get top n curves from %s...' % category
    #    get_top_n_curves_from_event_group(trfilenames, retfilename, trns, m, timeunit)

    #print 'get test curves...'
    #for category in categories:
    #    tefilenames = [event['path'] + '.eventtime.trw.common' for event in events if event['category'] == category and event['usage'] == 'Test']
    #    retfilename = os.path.join(retdirname, category + '.test.curves')
    #    tens = [-1 for _ in tefilenames]
    #    print 'get curves form %s...' % ', '.join([tefilename.rsplit('/', 1)[-1] for tefilename in tefilenames])
    #    get_top_n_curves_from_event_group(tefilenames, retfilename, tens, m, timeunit)

    print 'predict rtnums...'
    trfilenames = [os.path.join(retdirname, category + '.curves') for category in categories]
    tefilenames = [os.path.join(retdirname, category + '.test.curves') for category in categories]
    retfilenames = [os.path.join(retdirname, category + '.results') for category in categories]
    for trfilename, tefilename, retfilename in zip(trfilenames, tefilenames, retfilenames):
        print 'predict rtnums for %s...' % tefilename
        predict_rtnums(trfilename, tefilename, retfilename, simthreshold, pm)

