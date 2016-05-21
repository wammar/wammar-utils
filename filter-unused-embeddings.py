import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_embeddings", help=
                       " Input embeddings file (word2vec format).")
argparser.add_argument("-o", "--output_embeddings", help=
                       " Output embeddings file (word2vec format with no header).")
argparser.add_argument("-t", "--text", help=
                       " The text in this file will be tokenized on white spaces and used to determine whether to keep the embedding of a word or throw it away.")
args = argparser.parse_args()

# stream
with gzip.open(args.input_embeddings, mode='r') if args.input_embeddings.endswith('.gz') else open(args.input_embeddings, mode='r') as input_embeddings, gzip.open(args.text, mode='r') if args.text.endswith('.gz') else open(args.text, mode='r') as text, gzip.open(args.output_embeddings, mode='w') if args.output_embeddings.endswith('.gz') else open(args.output_embeddings, mode='w') as output_embeddings:

  text_vocab = set(text.read().decode('utf8').split(' '))
  text_vocab.add("UNK")
  text_vocab.add("<S>")
  text_vocab.add("<\S>")
  text_vocab.add("unk")
  text_vocab.add("<s>")
  text_vocab.add("<\s>")

  # read all words in the embeddings file
  embeddings_vocab = set()
  input_embeddings_counter, output_embeddings_counter = 0, 0
  for line in input_embeddings:
    try:
      line2 = line.decode('utf8')
    except UnicodeDecodeError:
      print 'WARNING: utf8 decoding error for the following line in the embeddings file:', line, '\nWill skip this one.'
      continue

    # filter out unused words
    input_embeddings_counter += 1
    if line2.strip().split(' ')[0] in text_vocab:
      output_embeddings_counter += 1
      output_embeddings.write(line) 

print 'input  embeddings counter =', input_embeddings_counter
print 'output embeddings counter =', output_embeddings_counter
