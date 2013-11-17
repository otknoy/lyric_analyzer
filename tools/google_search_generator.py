#!/usr/bin/env python

def extract_title(s):
    return s.split('\n')[1]

def extract_artist(s):
    return s.split('singer:\n')[-1].split('\n')[0]


def create_google_uri(query):
    return 'https://www.google.co.jp/search?q=' + query

def to_html(queries):
    str = '<html><body>'

    for q in queries:
        a =  '<p><a href="' + create_google_uri(q) + '">' + q + '</a></p>'
        str += a
    str += '</body></html>'

    return str


if __name__ == '__main__':
    import sys

    queries = []
    filenames = sys.argv[1:]
    for filename in filenames:
        f = open(filename)
        text = f.read()
        f.close()

        title = extract_title(text)
        artist = extract_artist(text)
        query = title + ' ' + artist
        queries.append(query)

    print to_html(queries)
