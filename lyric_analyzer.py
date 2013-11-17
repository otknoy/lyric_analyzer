#!/usr/bin/env python

import sys
path="../nlp"
sys.path.append(path)

import nlp
import k_means

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
        docs.append(doc.select_noun())

    text_collection = nlp.TextCollection(docs)
    tf = text_collection.tf
    tfidf = text_collection.tfidf


    # output tf of text collection
    # for t, f in sorted(tf.items(), key=lambda x:x[1]):
    #     print t, f

    for filename in filenames:
        print filename + '.tf'
        
    
    
    ## output term-document matrix
    # print 'term, ',
    # print ', '.join([f.split('/')[-1] for f in filenames])

    # for df in text_collection.df.keys():
    #     print df + ', ',
    #     print ', '.join([str(tfidf[df]) for tfidf in text_collection.tfidf])

    # for tfidf in text_collection.tfidf:
    #     print ', '.join([str(v) for v in tfidf.values()])


    
