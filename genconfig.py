#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

def genconfig(indirname, outfilename):
    with open(outfilename, 'w') as outfile:
        outfile.write('#!/usr/bin/env python\n')
        outfile.write('# -*- coding: utf-8 -*-\n')
        outfile.write('''
events = [
                ''')
        for name in os.listdir(indirname):
            infilename = os.path.join(indirname, name)
            if os.path.isfile(infilename):
                outfile.write('''
        {
           'name': "%s",
           'category': '',
           'time': '',
           'usage': 'Train',
           'path': "%s",
           },''' % (name, infilename))
        outfile.write(']')


if __name__ == '__main__':
    genconfig(sys.argv[1], sys.argv[2])
