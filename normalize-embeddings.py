import re
import time
import io
import sys
import argparse
from collections import defaultdict
import math

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input-embeddings", help=
                       " An input embeddings file (word2vec format).")
argparser.add_argument("-o", "--output-embeddings", help=
                       " An output embeddings file (word2vec format) where all vectors have an L2 norm of 1.0")
args = argparser.parse_args()

# stream
with gzip.open(args.output_embeddings, mode='w') if args.output_embeddings.endswith('.gz') else open(args.output_embeddings, mode='w') as output_file, gzip.open(args.input_embeddings, mode='r') if args.input_embeddings.endswith('.gz') else open(args.input_embeddings, mode='r') as input_file:
  # the first line of the embeddings file is metadata (word2vec format). throw it away.
  input_file.readline()
  # for each word cluster
  embeddings_count = 0
  embedding_dim = -1
  for line in input_file:
    try:
      line = line.decode('utf8')
    except UnicodeDecodeError:
      print 'WARNING: utf8 decoding error for the line:', line, '. Will skip this one.'
      continue
    # read the word and its embedding
    embeddings_count += 1
    line_splits = line.strip().split(' ')
    # check embedding size
    if embedding_dim == -1:
      embedding_dim = len(line_splits) - 1
    assert embedding_dim == len(line_splits) - 1
    sum_of_squares = 0.0
    vector = []
    # compute the normalizer
    for i in xrange(embedding_dim):
      value = float(line_splits[i+1])
      vector.append(value)
      sum_of_squares += value * value
    normalizer = math.sqrt(sum_of_squares)
    # normalize and round the floating number
    out_line_parts = [line_splits[0]]
    for i in xrange(embedding_dim):
      vector[i] /= normalizer
      out_line_parts.append(u'{0:.4f}'.format(vector[i]))
    # write to disk
    out_line = '{}\n'.format(u' '.join(out_line_parts).encode('utf8'))
    output_file.write(out_line)
