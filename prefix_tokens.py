import io
import argparse
import re

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-p", "--prefix", type=str, required=True, 
                       help="the string to prefix lines.")
args = argparser.parse_args()
prefix = args.prefix

with io.open(args.input_filename) as input_file, io.open(args.output_filename, mode='w') as output_file: 
  for line in input_file:
    tokens = line.strip().split(' ')
    for i in range(len(tokens)):
      tokens[i] = args.prefix + tokens[i]
    output_file.write(u'{}\n'.format(' '.join(tokens)))
