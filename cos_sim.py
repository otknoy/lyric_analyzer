#!/usr/bin/env python

import sys
path="../nlp"
sys.path.append(path)
import nlp

def extract_lyric(s):
    return s.split('lyric:\n')[-1]


if __name__ == '__main__':
    filenames = sys.argv[1:]

    lyrics = []
    for filename in filenames:
        f = open(filename)
        lyric = nlp.normalize(extract_lyric(f.read()).decode('utf-8'))
        f.close()
        lyrics.append(lyric)

    docs = []
    for lyric in lyrics:
        doc = nlp.mecab(lyric.encode('utf-8'))
        docs.append(doc)

    for i in range(len(docs)-1):
        d1 = docs[i]
        for j in range(i+1, len(docs)):
            if i == j: continue
            d2 = docs[j]
            cos_sim = d1.cos_similarity(d2)

            n1 = filenames[i].split('/')[-1]
            n2 = filenames[j].split('/')[-1]
            print "%s,%s,%f" % (1, n2, cos_sim)


    
