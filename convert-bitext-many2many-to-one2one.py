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

for line in input_file:
  splits = line.strip().split(args.delimiter)
  assert len(splits) == 2
  split0_elements, split1_elements = splits[0].split(' '), splits[1].split(' ')
  for split0_element in split0_elements:
    for split1_element in split1_elements:
      output_file.write(u'{}{}{}\n'.format(split0_element, args.delimiter, split1_element))

