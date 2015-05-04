import re
import time
import io
import sys
import argparse
from collections import defaultdict

# given two vocab files (one word type per line) vocab1, vocab2, find the differences vocab1 - vocab2 and vocab2 - vocab1 

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-v1", "--vocab1_filename", required=True)
argparser.add_argument("-v2", "--vocab2_filename", required=True)
argparser.add_argument("-v1m2", "--vocab1diff2_filename", required=True)
argparser.add_argument("-v2m1", "--vocab2diff1_filename", required=True)
args = argparser.parse_args()

vocab1 = set()
for line in io.open(args.vocab1_filename, encoding='utf8'):
  vocab1.add(line.strip())

vocab2 = set()
for line in io.open(args.vocab2_filename, encoding='utf8'):
  vocab2.add(line.strip())

with io.open(args.vocab1diff2_filename, encoding='utf8', mode='w') as vocab1diff2_file:
  vocab1diff2 = vocab1 - vocab2
  for word in vocab1diff2:
    vocab1diff2_file.write(u'{}\n'.format(word))

with io.open(args.vocab2diff1_filename, encoding='utf8', mode='w') as vocab2diff1_file:
  vocab2diff1 = vocab2 - vocab1
  for word in vocab2diff1:
    vocab2diff1_file.write(u'{}\n'.format(word))
