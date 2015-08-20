import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-k", required=True, type=int, help="the maximum number of pattern matches to show up in the output file.")
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-p", "--pattern", required=True, help="regular expression")
args = argparser.parse_args()

pattern = re.compile(args.pattern)

last_matched_index = 0
matches_count = 0
with io.open(args.input_filename, encoding='utf8') as input_file:
  data = input_file.read()

# skip the first k matches
new_match = False
while matches_count < args.k:
  new_match = pattern.search(data, last_matched_index)
  if not new_match: break
  matches_count += 1
  last_matched_index = new_match.end() - 1

# clip the data if necessary
if matches_count == args.k:
  data = data[:last_matched_index]

# write leftovers to output file
with io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  output_file.write(data)
