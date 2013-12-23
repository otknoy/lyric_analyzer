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
    ret = []
    for s in songs:
        y, m, d = s['year'].split('/')
        key = y
        if month: key += '/' + m
        ret.append(key)
    return ret

def classify_by_sex(songs):
    return [s['sex'] for s in songs]

def flatten(l):
    from itertools import chain
    return list(chain.from_iterable(l))


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

    # sex_labels = classify_by_sex(songs)

    docs = []
    for s in songs:
        text = nlp.normalize(s['lyric'])
        terms = nlp.tokenizer(text)
        terms = nlp.extract_noun(terms)
        terms = nlp.remove_stopword(terms)
        docs.append([t.basic_form for t in terms])


    # by year
    year_labels = classify_by_year(songs, month=False)
    year_docs = []
    labels = sorted(list(set(year_labels)))
    for label in labels:
        doc = flatten([d for d, l in zip(docs, year_labels) if l == label])
        year_docs.append(doc)

    # tf
    for l, d in zip(labels, year_docs):    
        tf = nlp.term_frequency(d)
        print l
        for t, w, in sorted(tf.items(), key=lambda x:-x[1])[:10]:
            print t.encode('utf-8'), w
        print

    exit()

    # tfidf
    tfidf_list = nlp.tf_idf(year_docs, normalize=True)
    for l, tfidf in zip(labels, tfidf_list):
        print l
        for t, w in sorted(tfidf.items(), key=lambda x:-x[1])[:10]:
            print t.encode('utf-8'), w
        print 
        
