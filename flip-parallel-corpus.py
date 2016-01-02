import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--delimiter", default=' ||| ', help="delimiter defaults to ' ||| '")
argparser.add_argument("-i", "--input_filename", help="parallel corpus (lang1, lang2)")
argparser.add_argument("-o", "--output_filename", help="parallel corpus (lang2, lang1)")
args = argparser.parse_args()

if args.delimiter.lower() == 'tab':
  args.delimiter = '\t'

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for line in input_file:
    splits = line.strip().split(args.delimiter)
    assert(len(splits) == 2)
    output_file.write(u'{}{}{}\n'.format(splits[1], args.delimiter, splits[0]))
