#!/usr/bin/env python

import sys
import nltk
import pickle
from   nltk.corpus import PlaintextCorpusReader
from   nltk.corpus import stopwords

def go(corpus, tf_file, minf):
    stopwds    = stopwords.words('english')
    TF         = {}
    wordlists  = PlaintextCorpusReader(corpus, '.*')

    for fileid in wordlists.fileids():
        text  = nltk.Text(nltk.word_tokenize(wordlists.raw(fileid)))
        words = [w.lower() for w in text if w.isalnum() and w.lower() not in stopwds and len(w) > 3]
        l     = float(len(words))

        TF[fileid] = {}
        for token in set(words):
            count = words.count(token)
            if count > minf: TF[fileid][token] = count / l

    pickle.dump(TF, open(tf_file, "wb"));
    fout = open(tf_file + ".csv", "wb")
    for k,v in TF.iteritems(): fout.write(str(k) + "," + str(v) + "\n")
    fout.close()

CORPUS_DIR = sys.argv[1]
MIN_FREQ   = int(sys.argv[3])
TF_FILE    = sys.argv[4]

if __name__ == '__main__':
    go(CORPUS_DIR, TF_FILE, MIN_FREQ)
