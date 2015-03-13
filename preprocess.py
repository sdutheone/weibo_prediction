#!/usr/bin python
import os
import sys
import compago
from utils import *

app = compago.Application()

#class TimeValidator:
#    def __init__(self, time1=None, time2=None):
#        self.time1 = time1
#        self.time2 = time2
#
#    def validate(self, line):
#        fields = get_fields(line)
#        time = fields['time']
#        return (not self.time1 or self.time1 <= time) and\
#                (not self.time2 or self.time2 >= time)

class OriTweetValidator:
    def __init__(self, time1=None, time2=None):
        self.time1 = time1
        self.time2 = time2
        self.mids = dict()

    def validate(self, line):
        fields = get_fields(line)
        time = fields['time']
        mid = fields['mid']
        rtmid = fields.get('rtMid', None)
        if rtmid:
            return rtmid in self.mids
        elif (not self.time1 or self.time1 <= time) and\
                (not self.time2 or self.time2 >= time):
            self.mids[mid] = True
            return True
        else:
            return False

def extract(indirname, outfilename, validator):
    n_read = 0L
    n_extracted = 0L
    outfile = open(outfilename, 'w')
    for name in os.listdir(indirname):
        infilename = os.path.join(indirname, name)
        if os.path.isfile(infilename):
            infile = open(infilename)
            for line in infile:
                if validator.validate(line):
                    outfile.write(line)
                    n_extracted += 1
                if n_extracted % 10000 == 0:
                    outfile.flush()
                    os.fsync(outfile.fileno())
                n_read += 1
                print '%d line(s) read. %d line(s) extracted' % (n_read, n_extracted)
            infile.close()
    outfile.close()

@app.option('-i', '--indirname', dest='indirname')
@app.option('-o', '--outfilename', dest='outfilename')
@app.option('-t1', '--time1', dest='time1')
@app.option('-t2', '--time2', dest='time2')
def extract_ori_tweets(indirname, outfilename, time1, time2):
    validator = OriTweetValidator(time1, time2)
    extract(indirname, outfilename, validator)

@app.option('-i', '--infilename', dest='infilename')
@app.option('-o', '--outdirname', dest='outdirname')
def split_file(infilename, outdirname):
    n_read = 0L
    n_read_total = 0L
    cur_time = None
    infile = open(infilename)
    outfile = None
    for line in infile:
        fields = get_fields(line)
        time = fields['time'].rsplit('-', 1)[0]
        if cur_time != time:
            n_read = 0L
            cur_time = time
            outfilename = os.path.join(outdirname, '%s.txt' % cur_time)
            if outfile:
                outfile.close()
            outfile = open(outfilename, 'w')
        outfile.write(line)
        n_read += 1
        n_read_total += 1
        if n_read % 100000 == 0:
            outfile.flush()
            os.fsync(outfile.fileno())
        print '%d line(s) in %s, %d line(s) in total.' % (n_read, cur_time, n_read_total)
    infile.close()
    outfile.close()


if __name__ == '__main__':
    app.run()
