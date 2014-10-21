#!/usr/bin/env python

import sys
import operator 
from   collections import defaultdict
#from   unidecode import unidecode ## Trouble??
import math
import nltk
from   nltk.corpus import PlaintextCorpusReader
from   nltk.corpus import stopwords

PRECLUDE_STOPWORDS   = False
OVERLOOK_STOPWORDS   = True
DOWNCASE             = True
BAD_CHARS            = "! @ # $ % ^ & * ( ) _ + - = { } [ ] | . \ : ; ' < > ? , / ~ ` \"".split()
VERY_BAD_CHARS       = "' \"".split()
CO_OCCURRENCE_WINDOW = 9
CLOSED_WORDS         = "non those thus with one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty were which was am what you yeah go who where when why 's is we i will this may until would should could a about above according across actually adj after afterwards again against all almost alone along already also although always among amongst an and another any anyhow anyone anything anywhere are around as at b be became because become becomes becoming been before beforehand begin behind being below beside besides between beyond both but by c can cannot caption co co. could d did do does down during e each eg eight eighty either else elsewhere end ending enough etc even ever every everyone everything everywhere except f few first for found from further g h had has have he hence her here hereafter hereby herein hereupon hers herself him himself his how however hundred i ie if in inc. indeed instead into is it its itself j k l last later latter latterly least less let like likely ltd m made make makes many maybe me meantime meanwhile might miss more moreover most mostly mr mrs much must my myself n namely neither never nevertheless next nine ninety no nobody none nonetheless noone nor not nothing now nowhere o of off often on once one only onto or other others otherwise our ours ourselves out over overall own p per perhaps q r rather recent recently s same seem seemed seeming seems seven several she should since so some somehow someone something sometime sometimes somewhere still such t to taking than that the their them themselves then thence there thereafter thereby therefore therein thereupon these they where your yours yourself yourselves z".split()

def get_co_occurrences(s,exact_match=False):
    r     = defaultdict(float)
    count = defaultdict(int)

    if (DOWNCASE): s = s.lower()

    for l in BAD_CHARS:
        s = s.replace(l, "")

    words = s.split()

    # Preclude stopwords?
    if (PRECLUDE_STOPWORDS):
        for c in CLOSED_WORDS:
            if (DOWNCASE):
                if (c in words):
                    sys.stderr.write(" Precluded stopword " + c + "\n")
                    words = [x for x in words if x != c]
            else: # To maintain capitalisation, only if !DOWNCASE:
                for w in words:
                    if (w.lower() == c.lower()):
                        sys.stderr.write(" Precluded stopword " + c + "\n")
                        words = [x for x in words if x != c]

    if (OVERLOOK_STOPWORDS):
        i = 0
        for t in words:
            count[t] += 1 # This is up here because sometimes `count is used for stuff that doesn not
                          # use OVERLOOK_STOPWORDS (ie. syntactic graphs)

            if (t in CLOSED_WORDS): continue

            start = max(i-CO_OCCURRENCE_WINDOW, 0)
            end   = min(i+CO_OCCURRENCE_WINDOW, len(words)-1)

            for w in words[start:end]:
                if (w != t and w not in CLOSED_WORDS): r[t + " " + w] += 1.0
            i += 1
    else:
        i = 0
        for t in words:
            start = max(i-CO_OCCURRENCE_WINDOW, 0)
            end   = min(i+CO_OCCURRENCE_WINDOW, len(words)-1)

            count[t] += 1
            for w in words[start:end]:
                if (w != t): r[t + " " + w] += 1.0
            i += 1

    if (len(r.keys()) > 0): return count,r
    else:                   return count,{}

## Normalise a discrete frequency distribution of a dictionary d so it:
#### 1) sums to 1
#### 2) is smoothed as a Krichevsky-Trofimov estimator (adds .5 to all counts and renorms)
# http://en.wikipedia.org/wiki/Krichevsky%E2%80%93Trofimov_estimator
def KT_norm(d):
    for k in d: d[k] += 0.5 # K-T smoothing

    s = sum(d.values())
    for k in d: d[k] /= s # Norm to sum(values) = 1
    
    return d

# Get the K-L divergence from set P to Q (P should be a baseline, as the function is not symetric).
def kl_div(a, b):
    p = a.copy()
    q = b.copy()
    keys = set(p.keys()) | set(q.keys())

    for k in keys:
        if (k not in p): p[k] = 0.0
        if (k not in q): q[k] = 0.0

    p = KT_norm(p)
    q = KT_norm(q)

    r = 0.0

    for k in keys:
        r += p[k] * math.log(p[k]/q[k]) # Definition of K-L Divergance

    return r

corpus = ""
corpus_file = sys.argv[1]
output_file = sys.argv[2]
fin = open(corpus_file,"r")
sys.stderr.write("----------------------------------\nReading in corpus ("+corpus_file+")...\n")
for line in fin:
    corpus += line
fin.close()

sys.stderr.write("Tokenizing...")
#corpus = unidecode(corpus)
#sys.stderr.write(".")
toks   = nltk.word_tokenize(corpus)
sys.stderr.write(".")
text   = nltk.Text(toks)
sys.stderr.write(".")
words  = [w.lower() for w in text if w.isalnum() and w.lower() not in CLOSED_WORDS and len(w) > 2]
sys.stderr.write(".\n")
TF     = {}

sys.stderr.write("Counting TF...\n")
for token in words:
    if token in TF: TF[token] += 1.0
    else:           TF[token]  = 1.0

sys.stderr.write("Retrieving co-occurrences...\n")
count,co_occurrences = get_co_occurrences(corpus)

CO  = {}

sys.stderr.write("Calculating K-L divergences...\n")
fout = open(output_file,'w')
fout.write("term,KL(tf,co),KL(co,tf),sym_KL_div\n")
for target in TF:
    if (TF[target] < 3): continue
    
    CO.clear()
    
    for co,f in co_occurrences.iteritems():
        w,t = co.split()
        
        if (w == target):
            if w in CO: CO[t] += f
            else:       CO[t]  = f

    kl1 = kl_div(TF,CO)
    kl2 = kl_div(CO,TF)
    
    fout.write(target + "," + str(kl1) + "," + str(kl2) + "," + str((kl1 + kl2) / 2.0) +  "\n")

fout.close()

exit(1)
