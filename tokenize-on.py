import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-after", nargs='+', action='append')
argparser.add_argument("-before", nargs='+', action='append')
argparser.add_argument("-beforeandafter", nargs='+', action='append')
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

nicknames = {'APOSTROPHE':'\'', 'HYPHEN':'-', 'PERIOD':'.', 'TAB':'\t'}

if len(args.after) > 0:
  for i in xrange(0, len(args.after[0])):
    if args.after[0][i] in nicknames:
      args.after[0][i] = nicknames[args.after[0][i]]

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for line in input_file:
    print 'INCOMPLETE IMPLEMENTATION' 
    
