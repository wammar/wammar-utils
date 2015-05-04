import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--delimiter", type=str, default=' ||| ', help="delimiter defaults to ' ||| '")
argParser.add_argument("-o", "--output-filename", type=str)
argParser.add_argument("-i", "--input-filename", type=str)
args = argParser.parse_args()

if args.delimiter.lower() == 'tab':
  args.delimiter = '\t'

output_file = io.open(args.output_filename, encoding='utf8', mode='w')
input_file = io.open(args.input_filename, encoding='utf8')

current_source = ''
current_targets = []
for line in input_file:
  splits = line.strip().split(args.delimiter)
  assert len(splits) == 2
  if current_source != splits[0]:
    if len(current_source) > 0:
      output_file.write(u'{}{}{}\n'.format(current_source, args.delimiter, u' '.join(current_targets)))
    current_source = splits[0]
    current_targets = []
  current_targets.append(splits[1])
output_file.write(u'{}{}{}\n'.format(current_source, args.delimiter, u' '.join(current_targets)))

output_file.close()
