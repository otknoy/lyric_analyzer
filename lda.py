#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        self.lyric = re.search(r'lyric:\n((?:.+\n)+)', text).group(1)

    def __str__ (self):
        return ', '.join([self.title, self.singer, self.writer, self.composer, self.year, self.sex]).encode('utf-8')

    def getDate(self, month=False):
        y, m, d = self.year.split('/')
        date = y
        if month: date += '/' + m
        return date


def flatten(l):
    """
    flatten two-dimensional list
    """
    from itertools import chain
    return list(chain.from_iterable(l))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='lyric analyzer')
    parser.add_argument('infile', nargs='*')
    args = parser.parse_args()
    filenames = args.infile

    songs = []
    for filename in filenames:
        song = SongInfo(filename)
        songs.append(song)

    for s in songs:
        text = nlp.normalize(s.lyric)
        terms = nlp.tokenizer(text)
        terms = nlp.extract_noun(terms)
        terms = nlp.remove_stopword(terms)
        s.terms = [t.basic_form for t in terms]

    texts = [s.terms for s in songs]
    # print '\n'.join(flatten(texts)).encode('utf-8')
    
    # gemsim lda
    import gensim
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(t) for t in texts]

    k = 10
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=k)

    for topic in lda.show_topics(-1, 15):
        print topic
    for s, topics_per_document in zip(songs, lda[corpus]):
        print s
        print topics_per_document
