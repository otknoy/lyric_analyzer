#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
path="../nlp"
sys.path.append(path)
import nlp


def load_lyric_file(filename):
    f = open(filename)
    text = nlp.normalize(f.read().decode('utf-8'))
    f.close()
    return ['\n'.join(e.split('\n')[1:]) for e in text.split('\n\n')]

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='lyric analyzer')
    parser.add_argument('infile', nargs='*')
    args = parser.parse_args()
    filenames = args.infile

    docs = []
    for filename in filenames:
       title, singer, writer, composer, year, sex, lyric = load_lyric_file(filename)
       terms = nlp.tokenizer(nlp.normalize(lyric))
       terms = nlp.extract_noun(terms)
       terms = nlp.remove_stopword(terms)
       # print ' '.join([t.basic_form for t in terms])
       docs.append([t.basic_form for t in terms] )

       
    # all tf
    print 'all tf'
    from itertools import chain
    all_doc = list(chain.from_iterable(docs))
    tf = nlp.term_frequency(all_doc)
    for t, f in sorted(tf.items(), key=lambda x:-x[1])[:10]:
        print "%s, %d" % (t.encode('utf-8'), f)
    print
        

    # tf
    print 'tf'
    for d in docs:
        print filenames[docs.index(d)]
        tf = nlp.term_frequency(d)
        for t, f in sorted(tf.items(), key=lambda x:-x[1])[:10]:
            print "%s, %d" % (t.encode('utf-8'), f)
    print
            

    # tfidf
    print 'tfidf'
    tfidf_list = nlp.tf_idf(docs)
    for tfidf in tfidf_list:
        print filenames[tfidf_list.index(tfidf)]
        for t, w in sorted(tfidf.items(), key=lambda x:-x[1])[:10]:
            print "%s, %f" % (t.encode('utf-8'), w)
