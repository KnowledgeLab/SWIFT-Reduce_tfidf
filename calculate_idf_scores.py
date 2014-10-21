#!/usr/bin/env python
import sys
import math
import operator
import pickle
from   time import sleep
from   collections import defaultdict

sleep(30)

def go(Tf_file, fileid, threshold):
    TF    = pickle.load(open(Tf_file, "rb"))
    docs  = float(len(TF.keys()))
    #docs  = 12 # WHAaatt!!???
    IDF   = defaultdict(float)

    for file in TF:
        for token in TF[file]: IDF[token] += 1 # Shouldn't this be TF[file][token] ?? This is counting 1 for every file token is found in, not it's frequency

    for token in [x for x in TF[fileid].keys()]:
        TF[fileid][token] *= math.log(docs / IDF[token])

    if (threshold == -1):
        for k,v in TF[fileid].iteritems():
            sys.stdout.write(KEY + "," + str(k) + "," + str(v) + "\n")
    else:
        for entry in (sorted(TF[fileid].iteritems(), key=operator.itemgetter(1))[-threshold:]):
            sys.stdout.write(KEY + "," + str(entry[0]) + "," + str(entry[1]) + "\n")

THRESHOLD  = int(sys.argv[1])
TF         = sys.argv[2]
KEY        = sys.argv[3].split('/')[-1]

if __name__ == '__main__':
    go(TF, KEY, THRESHOLD)
