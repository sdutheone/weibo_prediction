#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


def count_lines(pathname):
    nlines = 0L
    if os.path.isdir(pathname):
        for name in os.listdir(pathname):
            nlines += count_lines(os.path.join(pathname, name))
    else:
        with open(pathname) as infile:
            for line in infile:
                nlines += 1
    return nlines


if __name__ == '__main__':
    pathname = sys.argv[1]
    print count_lines(pathname)
