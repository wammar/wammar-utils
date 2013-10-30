import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-tokens", type=str, help="prune line if it has more than this many tokens")
argParser.add_argument("-in", "--input_filename", type=str, help="input filename")
argParser.add_argument("-out", "--output_filename", type=str, help="output filename")
argParser.add_argument("-ie", "--input_encoding", type=str, default='utf8')
argParser.add_argument("-oe", "--output_encoding", type=str, default='utf8')
args = argParser.parse_args()

counter = 0
of = io.open(args.output_filename, encoding=args.output_encoding, mode='w')
for line in io.open(args.input_filename, encoding=args.input_encoding, mode='r'):
  if len(line.split()) <= int(args.tokens):
    #print len(line.split())
    of.write(line)
  else:
    counter += 1

of.close()
print '{0} lines pruned out'.format(counter)
