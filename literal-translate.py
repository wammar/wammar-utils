import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--dictionary_filename", help="dictionary of source strings and corresponding target strings.")
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

dictionary = {}
with io.open(args.dictionary_filename, encoding='utf8') as dictionary_file:
  for line in dictionary_file:
    parts = line.split('|||')
    assert(len(parts) == 2)
    dictionary[parts[0].strip()] = parts[1].strip()

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:  
  for line in input_file:
    # space tokenize input sentences
    tokens = line.strip().split(' ')
    for i in xrange(len(tokens)):
      tokens[i] = dictionary[tokens[i]] if tokens[i] in dictionary else tokens[i]
    output_file.write(u'{}\n'.format(u' '.join(tokens)))

