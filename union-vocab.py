import re
import time
import io
import sys
import argparse
from collections import defaultdict

# given two vocab files (one word type per line) vocab1, vocab2, find the union vocab 

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i1", "--vocab1_filename", required=True)
argparser.add_argument("-i2", "--vocab2_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
args = argparser.parse_args()

union_vocab = set()
for line in io.open(args.vocab1_filename, encoding='utf8'):
  union_vocab.add(line.strip())

for line in io.open(args.vocab2_filename, encoding='utf8'):
  union_vocab.add(line.strip())

with io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for word in union_vocab:
    output_file.write(u'{}\n'.format(word))

