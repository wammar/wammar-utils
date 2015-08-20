import re
import time
import io
import sys
import argparse
from collections import defaultdict

# each line corresponds to the embedding of one cluster/closure of words which are translationally equivalent 
# from one or more languages. An example cluster of two words is "en:dog_|_fr:chien". If such cluster appears
# in the input file, the output file would have two separate lines, one for "en:dog", and another for 
# "fr:chien" with identical embeddings (i.e., the embedding of the cluster "en:dog_|_fr:chien" in the input 
# file.

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input-filename", help=
                       " An embeddings file (word2vec format) where the first column is a cluster/closure of words.")
argparser.add_argument("-o", "--output-filename", help=
                       " An embeddings file (word2vec format) where the first column corresponds to individual words.")
argparser.add_argument("-s", "--cluster-separator", default="_|_", help=
                       " Use this string to split between words which belong to the same" +
                       " cluster in the input file.")
argparser.add_argument("-g", "--ignore", action='store_true', help="ignore words which don't belong to a closure/cluster")
args = argparser.parse_args()

# stream
with gzip.open(args.output_filename, mode='w') if args.output_filename.endswith('.gz') else open(args.output_filename, mode='w') as output_file, gzip.open(args.input_filename, mode='r') if args.input_filename.endswith('.gz') else open(args.input_filename, mode='r') as input_file:
  # initialize
  unique_words = set()
  embedding_dimensionality = -1
  # the first line of the embeddings file is metadata (word2vec format). copy it as is.
  output_file.write(input_file.readline())
  # for each word cluster
  for line in input_file:
    try:
      line = line.decode('utf8')
    except UnicodeDecodeError:
      print 'WARNING: utf8 decoding error for the line:', line, '. Will skip this one.'
      continue    
    # read the cluster string and its embedding
    line_splits = line.strip().split(' ')
    # check embedding size
    if embedding_dimensionality == -1:
      embedding_dimensionality = len(line_splits) - 1
    if len(line_splits) == 2: 
      # skip (another?) metadata line
      continue
    if embedding_dimensionality != len(line_splits) - 1:
      print 'dimensionality problem: I thought the dimesnionality is {}, but this line has {} splits:\n{}'.format(embedding_dimensionality, len(line_splits), line_splits)
      assert False
    # merge embedding values back into a utf8-encoded string
    embedding_string = u' '.join(line_splits[1:]).encode('utf8')
    # split the cluster string into words
    cluster_splits = line_splits[0].split(args.cluster_separator)
    for i in xrange(len(cluster_splits)):
      word = cluster_splits[i]
      if i == len(cluster_splits) - 1:
        if len(word) < 5: continue
        if word.endswith('_|'): word = word[:-2]
        if word.endswith('_'): word = word[:-1]
      if word in unique_words:
        print u"WARNING: '{}' appears twice in input embeddings file. Will let go because the embeddings were apparently messed up. Please consider rebuilding your embeddings such that the cluster strings are not cut off. word2vec cuts off words of length > 1000 by default.".format(word)
      out_line = '{} {}\n'.format(word.encode('utf8'), embedding_string)
      # when -g is specified, don't write this line if the cluster is of size 1
      if args.ignore and len(cluster_splits) == 1: continue
      output_file.write(out_line)
    unique_words |= set(cluster_splits)
