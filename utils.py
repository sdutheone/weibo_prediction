#!/usr/bin python
import datetime
import math
import random
import sys

def get_fields(line):
    fields = dict()
    segs = line.strip().split('|#|')
    for seg in segs:
        key, value = seg.split(':', 1)
        fields[key] = value
    return fields


def pearson_corr(xs, ys):
    assert len(xs) == len(ys)
    assert len(xs) != 0

    xavg = sum(xs) / float(len(xs))
    yavg = sum(ys) / float(len(xs))
    a = 0.0
    b = 0.0
    c = 0.0
    corr = 0.0
    for x, y in zip(xs, ys):
        a += (x - xavg) * (y - yavg)
        b += (x - xavg) ** 2
        c += (y - yavg) ** 2
    if b * c != 0:
        corr = a / math.sqrt(b * c)
    return corr


if __name__ == '__main__':
    #timestr1 = sys.argv[1]
    #timestr2 = sys.argv[2]
    #print midpoint(timestr1, timestr2)

    #print common_user_num(sys.argv[1], sys.argv[2])

    xs = range(10)
    ys = range(10)
    random.shuffle(xs)
    random.shuffle(ys)
    print xs, ys
    print pearson_corr(xs, ys)
    print pearson_corr(range(10), range(10))
