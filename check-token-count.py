import re
import time
import io
import sys
import nltk
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-f1", "--filename1")
argParser.add_argument("-f2", "--filename2")
args = argParser.parse_args()

f1 = io.open(args.filename1, encoding='utf8')
f2 = io.open(args.filename2, encoding='utf8')
lines = 0
while True:
  lines += 1
  l1, l2 = f1.readline(), f2.readline()
  if len(l1.split(' ')) != len(l2.split(' ')): 
    print 'line #', lines, ' contains a different number of space-delimited tokens: ', len(l1.split(' ')), ' vs. ', len(l2.split(' '))
    print l1
    print l2
  if len(l1) == len(l2) and len(l1) == 0: break
