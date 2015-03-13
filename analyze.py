#!/usr/bin python
#-*- coding: utf-8 -*-
from utils import *
import compago
import datetime
import os

app = compago.Application()

class Analyzer:

    def collect(self, fields):
        raise NotImplementedError

    def analyze(self):
        raise NotImplementedError

    def save(self, filename):
        raise NotImplementedError

class PopAnalyzer(Analyzer):
    def __init__(self, seps=[10,50,100,500,1000,5000,10000]):
        self.seps = seps
        self.pops = dict()
        self.merged_pops = [0] * (len(seps) + 1)

    def collect(self, fields):
        mid = long (fields['mid'])
        rtmid = long (fields.get('rtMid', 0))
        if rtmid:
            self.pops[rtmid] += 1
        else:
            self.pops[mid] = 0

    def analyze(self):
        print len(self.pops)
        for pop in self.pops.values():
            for i, sep in enumerate(self.seps):
                if pop < sep:
                    self.merged_pops[i] += 1
                    break
            else:
                self.merged_pops[-1] += 1

    def save(self, filename):
        outfile = open(filename, 'w')
        outfile.write(str(self.seps) + '\n')
        outfile.write('\t'.join([str(pop) for pop in self.merged_pops]))
        outfile.write('\n')
        outfile.close()

class AvgNormPopAnalyzer(Analyzer):

    def __init__(self, duration=3*24*60, delta=10):
        self.duration = duration
        self.delta = delta
        self.n_delta = duration / delta
        self.tweets = dict()
        self.avgpops = [0.0] * (duration / delta + 1)
        self.n_retweeted = 0

    def collect(self, fields):
        duration = self.duration
        delta = self.delta
        n_delta = self.n_delta
        tweets = self.tweets

        timestr = fields['time']
        time = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        mid = long (fields['mid'])
        rtmid = long (fields.get('rtMid', 0))

        if rtmid:
            tweet = tweets[rtmid]
            t_delta = time - tweet[0]
            index = t_delta.days * (24 * 60 / delta) + t_delta.seconds / (60 * delta) + 1
            if index <= n_delta:
                if tweet[2][-1][0] != index:
                    tweet[2].append([index, 1])
                else:
                    tweet[2][-1][1] += 1
                tweet[1] += 1
        else:
            tweets[mid] = [time, 0, [[0, 0]]] # [发布时间, 转发次数, [[时间段, 转发次数]]]

    def analyze(self):
        n_delta = self.n_delta
        avgpops = self.avgpops
        for tweet in self.tweets.values():
            n_retweets = tweet[1]
            pops = tweet[2]
            for i in range(len(pops) - 1):
                pops[i + 1][1] += pops[i][1]
            if n_retweets != 0:
                start = 0
                for i in range(len(pops)):
                    pops[i][1] = pops[i][1] / float (n_retweets)
                    end = pops[i][0]
                    for j in range(start, end + 1):
                        avgpops[j] += pops[i][1]
                    start = end + 1
                for i in range(start, n_delta + 1):
                    avgpops[i] += pops[-1][1]
                self.n_retweeted += 1
        for i in range(len(avgpops)):
            avgpops[i] /= self.n_retweeted

    def save(self, filename):
        outfile = open(filename, 'w')
        outfile.write('%d retweeted.\n' % self.n_retweeted)
        outfile.write('average popularity\t')
        outfile.write('\t'.join([str(pop) for pop in self.avgpops]))
        outfile.write('\n')
        for mid, (_, n_retweets, pops) in self.tweets.items():
            outfile.write('%d\t%d\t' % (mid, n_retweets))
            outfile.write('\t'.join([str(pop) for pop in pops]))
            outfile.write('\n')
        outfile.close()

@app.option('-i', '--infilename', dest='infilename')
@app.option('-o', '--outdirname', dest='outdirname')
def analyze(infilename, outdirname, p=False, anp=False):
    analyzers = []
    if p:
        analyzers.append(PopAnalyzer())
    if anp:
        analyzers.append(AvgNormPopAnalyzer())

    infile = open(infilename)
    for line in infile:
        fields = get_fields(line)
        #try:
        for analyzer in analyzers:
            analyzer.collect(fields)
        #except Exception as e:
            #print e.message
            #print line
    infile.close()

    for analyzer in analyzers:
        outfilename = os.path.join(outdirname, analyzer.__class__.__name__)
        analyzer.analyze()
        analyzer.save(outfilename)


if __name__ == '__main__':
    app.run()
