#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
path="../nlp"
sys.path.append(path)
import nlp

import re


def load_lyric_file(filename):
    f = open(filename)
    text = nlp.normalize(f.read().decode('utf-8'))
    f.close()
    # return ['\n'.join(e.split('\n')[1:]) for e in text.split('\n\n')]
    ret = {}
    for e in text.split(u'\n\n'):
        label, s = e.split(u':\n')
        ret[label] = s
    return ret

def classify_by_year(songs, month=False):
    ret = {}
    for s in songs:
        y, m, d = s['year'].split('/')
        key = y
        if month: key += '/' + m
        if not ret.has_key(key):
            ret[key] = []
        ret[key].append(s)
    return ret

def classify_by_sex(songs):
    ret = {}
    for s in songs:
        key = s['sex']
        if not ret.has_key(key):
            ret[key] = []
        ret[key].append(s)
    return ret


def lsa(matrix, dim):
    import sklearn.decomposition
    import sklearn.preprocessing
    lsa = sklearn.decomposition.TruncatedSVD(dim)
    matrix = lsa.fit_transform(matrix)
    matrix = sklearn.preprocessing.Normalizer(copy=False).fit_transform(matrix)
    return matrix

def kmeans(matrix, k=10):
    import sklearn.cluster
    km  = sklearn.cluster.KMeans(n_clusters=k, init='k-means++', n_init=1, verbose=True)
    km.fit(matrix).labels
    return km
    # labels = km.labels_
    # print labels
    # for f, l in sorted(zip(filenames, labels), key=lambda x:x[1]):
    #     print l, f.split('/')[-1].split('.')[0]

                
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='lyric analyzer')
    parser.add_argument('infile', nargs='*')
    args = parser.parse_args()
    filenames = args.infile

    songs = []
    for filename in filenames:
        song = load_lyric_file(filename)
        songs.append(song)

    by_year = classify_by_year(songs, month=False)
    by_sex = classify_by_sex(songs)

    # print by_year.keys()
    # print by_sex.keys()

    docs = []
    for sex, songs in by_year.items():
        text = '\n'.join([s['lyric'] for s in songs]) 
        text = nlp.normalize(text)
        terms = nlp.tokenizer(text)
        terms = nlp.extract_noun(terms)
        terms = nlp.remove_stopword(terms)
        docs.append([t.basic_form for t in terms])

    # tf
    for label, doc in sorted(zip(by_year.keys(), docs), key=lambda x:x[0]):
        print label
        tf = nlp.term_frequency(doc, normalize=True)
        for t, w, in sorted(tf.items(), key=lambda x:-x[1])[:10]:
            print t.encode('utf-8'), w
        print

    
    # all tf
    from itertools import chain
    all_doc = list(chain.from_iterable(docs))
    tf = nlp.term_frequency(all_doc)
    print "word,count"
    for t, f in sorted(tf.items(), key=lambda x:-x[1]):
        print "%s, %d" % (t.encode('utf-8'), f)
    print

    

    import numpy 
    matrix = numpy.array([e.values() for e in corpus])
    matrix = lsa(matrix, dim=20)
    km = kmeans(matrix, k=10)

    labels = km.labels_
    print labels
    for f, l in sorted(zip(filenames, labels), key=lambda x:x[1]):
        print l, f.split('/')[-1].split('.')[0]
