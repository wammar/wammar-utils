import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", help="input file")
argparser.add_argument("-o", "--output_filename", help="output file, with stripped lines")
args = argparser.parse_args()

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for line in input_file:
    output_file.write(line.strip()+u'\n')

