import argparse
import re
import time
import io
import sys
from collections import defaultdict
from itertools import izip
import os

argparser = argparse.ArgumentParser()
argparser.add_argument("-e", "--embeddings-file")
args = argparser.parse_args()

with gzip.open(args.embeddings_file, mode='r') if args.embeddings_file.endswith('.gz') else open(args.embeddings_file, mode='r') as input_file:
  vector_size = -1
  lines_counter = 0
  for line in input_file:
    lines_counter += 1
    if vector_size == -1:
      vector_size = len(line.strip().split(' ')) - 1
    else:
      assert(len(line.strip().split(' ')) - 1 == vector_size)

with gzip.open(args.embeddings_file, mode='r') if args.embeddings_file.endswith('.gz') else open(args.embeddings_file, mode='r') as input_file, gzip.open(args.embeddings_file + "TeMp", mode='w') if args.embeddings_file.endswith('.gz') else open(args.embeddings_file + "TeMp", mode='w') as output_file:
  output_file.write('{} {}\n'.format(lines_counter, vector_size))
  for line in input_file:
    output_file.write(line)

os.rename(args.embeddings_file+"TeMp", args.embeddings_file)
