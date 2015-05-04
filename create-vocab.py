import re
import time
import io
import sys
import argparse
from collections import defaultdict

# splits tokens on a whitespace, and outputs unique tokens

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-l", "--lowercase", action='store_true')
argparser.add_argument("-c", "--count", action='store_true')
argparser.add_argument("-e", "--encoding", action='store_true')
argparser.add_argument("-np", "--no_punctuation", action='store_true')
args = argparser.parse_args()

tokenizedCorpus = io.open(args.input_filename, encoding='utf8', mode='r')
vocabFile = io.open(args.output_filename, encoding='utf8', mode='w')

vocab = defaultdict(int)
for line in tokenizedCorpus:
  tokens = line.strip().split(' ')
  for token in tokens:
    token = token.lower()
    if args.no_punctuation and not token.isalnum():
      continue
    vocab[token] += 1

encoding = 0
for key in vocab.keys():
  if args.encoding:
    vocabFile.write(u'{0} '.format(encoding))
  vocabFile.write(u'{0}'.format(key))
  if args.count:
    vocabFile.write(u' {}'.format(vocab[key]))
  vocabFile.write(u'\n')
  encoding += 1

tokenizedCorpus.close()
vocabFile.close()
