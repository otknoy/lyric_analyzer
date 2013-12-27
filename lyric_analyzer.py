#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import nlp


class SongInfo:
    def __init__(self, filename):
        f = open(filename)
        text = nlp.normalize(f.read().decode('utf-8'))
        f.close()
        self.title = re.search(r'title:\n(.+)\n', text).group(1)
        self.singer = re.search(r'singer:\n(.+)\n', text).group(1)
        self.writer = re.search(r'writer:\n(.+)\n', text).group(1)
        self.composer = re.search(r'composer:\n(.+)\n', text).group(1)
        self.year = re.search(r'year:\n(.+)\n', text).group(1)        
        self.sex = re.search(r'sex:\n(.+)\n', text).group(1)
        self.lyric = re.search(r'lyric:\n((?:.+\n)+)', text).group()

    def __str__ (self):
        return ', '.join([self.title, self.singer, self.writer, self.composer, self.year, self.sex]).encode('utf-8')

    def getDate(self, month=False):
        y, m, d = self.year.split('/')
        date = y
        if month: date += '/' + m
        return date


def distribution(labels):
    """
    return label distribution
    """
    ret = {}
    for l in sorted(list(set(labels))):
        ret[l] = labels.count(l)
    return ret

def flatten(l):
    """
    flatten two-dimensional list
    """
    from itertools import chain
    return list(chain.from_iterable(l))


def lsa(matrix, dim):
    """
    Latent Semantic Analysis
    """
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
        # song = load_lyric_file(filename)
        song = SongInfo(filename)
        songs.append(song)

    docs = []
    for s in songs:
        text = nlp.normalize(s.lyric)
        terms = nlp.tokenizer(text)
        terms = nlp.extract_noun(terms)
        terms = nlp.remove_stopword(terms)
        s.terms = [t.basic_form for t in terms]

    # dist = distribution([s.getDate(month=True) for s in songs])
    # for k, v in sorted(dist.items()):
    #     print k, v
    # dist = distribution([s.sex for s in songs])
    # for k, v in sorted(dist.items()):
    #     print k, v

    # by year
    year_labels = [s.getDate() for s in songs]
    year_docs = {}
    labels = sorted(list(set(year_labels)))
    for label in labels:
        terms = flatten([s.terms for s in songs if s.getDate(month=True) == label])
        year_docs[label] = terms

    # tf
    # for l, d in year_docs.items():
    #     tf = nlp.term_frequency(d, normalize=True)
    #     # n = len([s for s in songs if s['year'] == l])
    #     # print "%s: %d songs" % (l, n)
    #     print l.encode('utf-8')
    #     for t, w, in sorted(tf.items(), key=lambda x:-x[1])[:10]:
    #         print t.encode('utf-8'), w
    #     print

    # tfidf
    tfidf_list = nlp.tf_idf(year_docs.values(), normalize=True)
    for l, tfidf in zip(labels, tfidf_list)[-15:]:
        print l
        for t, w in sorted(tfidf.items(), key=lambda x:-x[1])[:10]:
            print t.encode('utf-8'), w
        print 
        
