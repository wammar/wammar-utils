import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True, help="parallel corpus (lang1, lang2)")
argparser.add_argument("-o", "--output_filename", required=True, help="parallel corpus (lang2, lang1)")
argparser.add_argument("-s", "--new_size", type=int, required=True, help="size of the embeddings in the output file")
args = argparser.parse_args()

assert(args.new_size > 0)

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  first_line = True
  for line in input_file:
    splits = line.strip().split(' ')
    if first_line and len(splits) == 2: continue
    first_line = False
    old_size = len(splits) - 1
    assert(old_size > 1)
    if args.new_size <= old_size:
      splits = splits[:args.new_size + 1]
    else:
      while len(splits) - 1 < args.new_size:
        splits.append('0.0')
    output_file.write(u'{}\n'.format(u' '.join(splits)))
