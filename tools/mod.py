#!/usr/bin/env python

if __name__ == '__main__':
    import sys

    filenames = sys.argv[1:]
    for filename in filenames:
        f = open(filename)
        text = f.read()
        f.close()

        f = open(filename, 'w')
        f.write(text.replace('singe:\n', 'singer:\n'))
        f.close()
