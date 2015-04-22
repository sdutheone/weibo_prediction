#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


def collect_results(infilename, errthreshold):
    '''
    统计预测结果
    infilename: 预测结果文件
    '''
    correct = 0
    total = 0

    with open(infilename) as infile:
        for line in infile:
            segs = line.strip().split()
            if float(segs[1]) <= errthreshold:
                correct += 1
            total += 1

    return correct, total


def calculate_precisions(infilenames, errthreshold):
    correct_overall = 0
    total_overall = 0
    for infilename in infilenames:
        correct, total = collect_results(infilename, errthreshold)
        precision = 0.0 if total == 0 else float(correct) / total
        print infilename, correct, total, precision
        correct_overall += correct
        total_overall += total
    precision_overall = 0.0 if total_overall == 0 else float(correct_overall) / total_overall
    print 'overall', correct_overall, total_overall, precision_overall


if __name__ == '__main__':
    errthreshold = float(sys.argv[1])
    infilenames = sys.argv[2: ]
    calculate_precisions(infilenames, errthreshold)
