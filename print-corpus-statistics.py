import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", help="corpus")
argparser.add_argument("-o", "--output_filename", help="stats")
args = argparser.parse_args()

word2freq = {}
with io.open(args.input_filename, encoding='utf8') as input_file:
  for line in input_file:
    tokens = line.strip().split()
    for token in tokens:
      if token not in word2freq: word2freq[token] = 0
      word2freq[token] += 1

freq2word_count = defaultdict(int)
max_freq = 0
for word in word2freq.keys():
  freq2word_count[word2freq[word]] += 1
  max_freq = max(max_freq, word2freq[word])

with io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  output_file.write(u'freq\tnumber of words with this freq\tnumber of words with at least this frequency\n')
  total = 0
  for freq in reversed(range(1, max_freq+1)):
    if freq not in freq2word_count: continue
    total += freq2word_count[freq]
    output_file.write(u'{}\t{}\t{}\n'.format(freq, freq2word_count[freq], total))
