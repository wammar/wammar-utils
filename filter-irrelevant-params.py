import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-ci", "--case_insensitive")
argparser.add_argument("-ip", "--input_filename")
argparser.add_argument("-iw", "--input_word_types_filename")
argparser.add_argument("-op", "--output_filename")
args = argparser.parse_args()

relevant_params = set()

input_word_types_file = io.open(args.input_word_types_filename, encoding='utf8')
for line in input_word_types_file:
  if args.case_insensitive:
    line = line.lower()
  relevant_params.add(tuple(line.split()[:-1]))
input_word_types_file.close()

assert(len(relevant_params) > 0)

input_file = io.open(args.input_filename, encoding='utf8')
output_file = io.open(args.output_filename, encoding='utf8', mode='w')
for original_line in input_file:
  if args.case_insensitive:
    line = original_line.lower()
  else:
    line = original_line
  param_id = tuple(line.split()[:-1])
  if param_id in relevant_params:
    output_file.write(line)
input_file.close()
output_file.close()
