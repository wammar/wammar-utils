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
argParser.add_argument("-i1", "--input1-filename", type=str)
argParser.add_argument("-i2", "--input2-filename", type=str, default='utf8')
args = argParser.parse_args()

if args.delimiter.lower() == 'tab':
  args.delimiter = '\t'

output_file = io.open(args.output_filename, encoding='utf8', mode='w')
input1_file = io.open(args.input1_filename, encoding='utf8')
input2_file = io.open(args.input2_filename, encoding='utf8')

# create a map for the second corpus
corpus2 = defaultdict(list)
input2_counter = 0
for line in input2_file:
  splits = line.strip().split(args.delimiter)
  assert len(splits) == 2
  corpus2[splits[0]].append(splits[1])
  input2_counter += 1
print input2_counter, 'lines were read from ', args.input2_filename

input1_counter, output_counter = 0, 0
# scan first corpus, and write the output corpus
for line in input1_file:
  splits = line.strip().split(args.delimiter)
  assert len(splits) == 2
  input1_counter += 1
  if splits[1] not in corpus2: continue
  for corpus2_target in corpus2[ splits[1] ]:
    output_file.write(u'{}{}{}\n'.format(splits[0], args.delimiter, corpus2_target))
    output_counter += 1

print input1_counter, 'lines processed from', args.input1_filename
print output_counter, 'lines written to', args.output_filename

