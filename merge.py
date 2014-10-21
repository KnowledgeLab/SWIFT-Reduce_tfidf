#!/usr/bin/env python

import sys
import pickle

if __name__ == '__main__':
    OUTPUT = sys.argv[1]
    ACCUM  = pickle.load(open(sys.argv[2],"rb"))

    for i in sys.argv[3:]: ACCUM.update(pickle.load(open(i,"rb")))

    pickle.dump(ACCUM, open(OUTPUT, "wb"));
