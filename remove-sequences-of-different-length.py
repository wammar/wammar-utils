import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i1", help="input token sequences")
argparser.add_argument("-i2", help="input label sequences")
argparser.add_argument("-o1", help="output token sequences")
argparser.add_argument("-o2", help="output label sequences")
args = argparser.parse_args()

with io.open(args.i1, encoding='utf8') as in1_file, io.open(args.i2, encoding='utf8') as in2_file, io.open(args.o1, encoding='utf8', mode='w') as out1_file, io.open(args.o2, encoding='utf8') as out2_file:
  valid_counter, all_counter = 0, 0
  for l1 in in1_file:
    l2 = in2_file.readline()
    all_counter += 1
    if len(l1.split(' ')) != len(l2.split(' ')): continue
    out1_file.write(l1)
    out2_file.write(l2)
    valid_counter += 1

in1_file.close()
in2_file.close()
out1_file.close()
out2_file.close()

print '{} valid lines written out of {} total lines'.format(valid_counter, all_counter)
