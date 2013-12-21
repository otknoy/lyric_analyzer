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

def classify_by_year(info):
    ret = {}
    for i in info:
        y, m, d = i['year'].split('/')
        key = y + '/' + m
        if not ret.has_key(key):
            ret[key] = []
        ret[key].append(i)
    return ret

def classify_by_sex(info):
    ret = {}
    for i in info:
        sex = i['sex']
        if not ret.has_key(sex):
            ret[sex] = []
        ret[sex].append(i)
    return ret
    

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

    by_year = classify_by_year(songs)
    by_sex = classify_by_sex(songs)

    docs_year = {}
    for year, d in sorted(by_year.items()):
        lyric = '\n'.join([e['lyric'] for e in d])
        lyric = nlp.normalize(lyric)
        terms = nlp.tokenizer(lyric)
        terms = nlp.extract_noun(terms)
        terms = nlp.remove_stopword(terms)
        docs_year[year] = [t.basic_form for t in terms]

    for year, d in sorted(docs_year.items()):
        print "%s, %d" % (year, len(by_year[year]))
        # tf = nlp.term_frequency(d)
        # for t, f in sorted(tf.items(), key=lambda x:-x[1]):
        #     print t.encode('utf-8'), f
        # print 
        


    exit()

    
    docs = []
    male = []
    female = []
    for d in data:
        terms = nlp.tokenizer(nlp.normalize(d['lyric']))
        terms = nlp.extract_noun(terms)
        terms = nlp.remove_stopword(terms)
        if d['sex'] == 'male':
            male.append([t.basic_form for t in terms])
        elif d['sex'] == 'female':
            female.append([t.basic_form for t in terms])
        docs.append([t.basic_form for t in terms])

    # print len(filenames)
    # print len(male)
    # print len(female)
       
    # all tf
    from itertools import chain
    all_doc = list(chain.from_iterable(docs))
    tf = nlp.term_frequency(all_doc)
    print "word,count"
    for t, f in sorted(tf.items(), key=lambda x:-x[1]):
        print "%s, %d" % (t.encode('utf-8'), f)
    print

    exit()

    # tf
    # print 'tf'
    # for d in docs:
    #     print filenames[docs.index(d)]
    #     tf = nlp.term_frequency(d)
    #     for t, f in sorted(tf.items(), key=lambda x:-x[1])[:10]:
    #         print "%s, %d" % (t.encode('utf-8'), f)
    # print
            

    # tfidf
    print 'tfidf'
    tfidf_list = nlp.tf_idf(docs)
    for tfidf in tfidf_list:
        print filenames[tfidf_list.index(tfidf)]
        for t, w in sorted(tfidf.items(), key=lambda x:-x[1])[:10]:
            print "%s, %f" % (t.encode('utf-8'), w)


    exit()
    
    # kmeans
    import numpy
    matrix = numpy.array([e.values() for e in tfidf_list])
    import sklearn.decomposition
    import sklearn.preprocessing
    dim = 20
    lsa = sklearn.decomposition.TruncatedSVD(dim)
    matrix = lsa.fit_transform(matrix)
    matrix = sklearn.preprocessing.Normalizer(copy=False).fit_transform(matrix)

    import sklearn.cluster
    k = 30
    km  = sklearn.cluster.KMeans(n_clusters=k, init='k-means++', n_init=1, verbose=True)
    km.fit(matrix)
    labels = km.labels_

    print labels
    for f, l in sorted(zip(filenames, labels), key=lambda x:x[1]):
        print l, f.split('/')[-1].split('.')[0]
    
            
