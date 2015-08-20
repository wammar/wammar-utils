import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-e", "--embeddings", help=
                       " An embeddings file (word2vec format).")
argparser.add_argument("-t", "--text", help=
                       " The text in this file will be tokenized on white spaces and used to measure coverage.")
args = argparser.parse_args()

# stream
with gzip.open(args.embeddings, mode='r') if args.embeddings.endswith('.gz') else open(args.embeddings, mode='r') as embeddings, gzip.open(args.text, mode='r') if args.text.endswith('.gz') else open(args.text, mode='r') as text:

  # read all words in the embeddings file
  embeddings_vocab = set()
  for line in embeddings:
    try:
      line = line.decode('utf8')
    except UnicodeDecodeError:
      print 'WARNING: utf8 decoding error for the following line in the embeddings file:', line, '\nWill skip this one.'
      continue
    embeddings_vocab.add(line.strip().split(' ')[0])
 
  # read each token in the text file
  tokens_covered, tokens_uncovered = 0, 0
  types_covered, types_uncovered = 0, 0
  text_vocab = set()
  frequency_of_uncovered_types = defaultdict(int)
  for line in text:
    try:
      line = line.decode('utf8')
    except UnicodeDecodeError:
      print 'WARNING: utf8 decoding error for the following line in the embeddings file:', line, '\nWill skip this one.'
      continue

    # for each token in the file
    for token in line.strip().split():

      # word found in the embeddings
      if token in embeddings_vocab: 
        tokens_covered += 1 
        
        # is it a new word type?
        if token not in text_vocab: types_covered += 1

      # word not found in the embeddings
      else: 
        tokens_uncovered += 1

        # is it a new word type?
        if token not in text_vocab: 
          types_uncovered += 1

        # count frequency of uncovered word types
        frequency_of_uncovered_types[token] += 1


      # this is no longer a new word type
      text_vocab.add(token)

print 'token coverage =', tokens_covered, '/', tokens_covered + tokens_uncovered, '=', 1.0 * tokens_covered / (tokens_covered + tokens_uncovered)
print 'type coverage  =', types_covered, '/', types_covered + types_uncovered, '=', 1.0 * types_covered / (types_covered + types_uncovered)
print 'most frequent uncovered word types =', sorted(frequency_of_uncovered_types.iteritems(),key=lambda (k,v): v,reverse=True)[:30] 
