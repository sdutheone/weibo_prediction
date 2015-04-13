#!/usr/bin python
# -*- coding: utf-8 -*-
import networkx as nx
import os
import sys


def split_finalsn(infilename, outdirname):
    
    outfiles = {}
    numstrs = [str(_) for _ in range(10)]
    names = [i + j + k for i in numstrs for j in numstrs for k in numstrs]
    for name in names:
        outfiles[name] = open(os.path.join(outdirname, name), 'w')

    with open(infilename) as infile:
        for line in infile:
            followee = line.strip().split()[1]
            outfiles[followee[-3: ]].write(line)


if __name__ == '__main__':
    infilename = sys.argv[1]
    outdirname = sys.argv[2]
    split_finalsn(infilename, outdirname)
