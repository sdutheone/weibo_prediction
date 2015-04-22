#!/usr/bin python
# -*- coding: utf-8 -*-
import datetime
import os

import networkx as nx


def get_follower_uids(fsdirname, followee_uid):
    
    fsfilename = fsdirname
    for s in followee_uid[-4: ]:
        fsfilename = os.path.join(fsfilename, s)
    fsfilename = os.path.join(fsfilename, followee_uid + '.fs')

    follower_uids = set()
    if os.path.exists(fsfilename):
        with open(fsfilename) as fsfile:
            for line in fsfile:
                follower_uid = line.strip()
                follower_uids.add(follower_uid)
    
    return follower_uids


def calculate_user_influences(fsdirname, uids):
    
    uids_to_process = set(uids)
    uids_processed = set()
    G = nx.DiGraph()

    while uids_to_process:
        uid = uids_to_process.pop()
        if uid not in uids_processed:
            follower_uids = get_follower_uids(fsdirname, uid)
            edges = [(follower_uid, uid) for follower_uid in follower_uids]
            G.add_edges_from(edges)
            uids_to_process = uids_to_process.union(follower_uids)
            uids_processed.add(uid)

    node2score = leaderrank(G)

    return node2score


def leaderrank(G):
    
    ground = 'ground'

    node2score = {}
    node2scoretmp = {}
    node2score[ground] = 0.0
    node2scoretmp[ground] = 0.0

    for node in G:
        G.add_edge(ground, node)
        G.add_edge(node, ground)
        node2score[node] = 1.0
        node2scoretmp[node] = 1.0

    iteration = 1
    while iteration <= 20:
        print 'iteration %d' % iteration
        for node in G:
            score = 0.0
            for prenode in G.predecessors_iter(node):
                prescore_ = node2score[prenode]
                kout = len(G.successors_iter(prenode))
                score += prescore / kout
            node2scoretmp[node] = score
        node2score.update(node2scoretmp)
        iteration += 1

    G.remove_node(ground)
    node2score.pop(ground)

    score = node2scoretmp[ground] / len(G)
    for node in node2score:
        node2score[node] += score

    return node2score


if __name__ == '__main__':
    G = nx.DiGraph()
    G.add_node('ground', time='dddd')
    print G.node['ground']
