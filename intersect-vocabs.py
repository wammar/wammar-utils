import re
import time
import io
import sys
import argparse
from collections import defaultdict
import gzip

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_vocabs", help=
                       " Comma-separated list of text files.")
argparser.add_argument("-o", "--output_vocab", help=
                       " Output vocab file, one word per line, which only includes words which appear in each of the input files.")
args = argparser.parse_args()

vocabs = []
input_vocab_filenames = args.input_vocabs.split(',')
for input_vocab_filename in input_vocab_filenames:
  with gzip.open(input_vocab_filename, mode='r') if input_vocab_filename.endswith('.gz') else open(input_vocab_filename, mode='r') as input_vocab:
    vocab = set(input_vocab.read().split())
    print '{} unique words found in {}'.format(len(vocab), input_vocab_filename)
    vocabs.append(vocab)

# find intersection
intersection = vocabs[0]
for i in xrange(1, len(vocabs)):
  intersection &= vocabs[i]

# write to output file 
with gzip.open(args.output_vocab, mode='w') if args.output_vocab.endswith('.gz') else open(args.output_vocab, mode='w') as output_vocab_file:
  output_vocab_file.write('\n'.join(intersection))

print '{} unique words found in the intersection. written to {}'.format(len(intersection), args.output_vocab)
