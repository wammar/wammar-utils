import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input-embeddings", help=
                       " An embeddings file (word2vec format).")
argparser.add_argument("-o", "--output-embedding", help=
                       " Output file (word2vec format) with only one line which represents the average embedding in the input file.")
args = argparser.parse_args()

# stream
with gzip.open(args.output_embedding, mode='w') if args.output_embedding.endswith('.gz') else open(args.output_embedding, mode='w') as output_file, gzip.open(args.input_embeddings, mode='r') if args.input_embeddings.endswith('.gz') else open(args.input_embeddings, mode='r') as input_file:
  # the first line of the embeddings file is metadata (word2vec format). throw it away.
  input_file.readline()
  # for each word cluster
  summation = []
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
      for i in xrange(embedding_dim):
        summation.append(0.0)
    assert embedding_dim == len(line_splits) - 1
    for i in xrange(embedding_dim):
      summation[i] += float(line_splits[i+1])

  # Compute the average
  for i in xrange(len(summation)):
    summation[i] = str(summation[i] / embeddings_count)

  # write to output file
  out_line = '{} {}\n'.format('avg', ' '.join(summation).encode('utf8'))
  output_file.write(out_line)
  
