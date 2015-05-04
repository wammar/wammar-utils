import argparse
import re
import time
import io
import sys
from collections import defaultdict
from itertools import izip

argparser = argparse.ArgumentParser()
argparser.add_argument("-pi", "--parallel-input")
argparser.add_argument("-si", "--source-input")
argparser.add_argument("-ti", "--target-input")
argparser.add_argument("-po", "--parallel-output")
argparser.add_argument("-so", "--source-output")
argparser.add_argument("-to", "--target-output")
argparser.add_argument("-sml", "--source-max-length", type=int, default=10)
argparser.add_argument("-tml", "--target-max-length", type=int, default=10) 
args = argparser.parse_args()

srcCorpusIn = io.open(args.source_input, encoding='utf8', mode='r') if args.source_input else None
tgtCorpusIn = io.open(args.target_input, encoding='utf8', mode='r') if args.target_input else None
pllCorpusIn = io.open(args.parallel_input, encoding='utf8', mode='r') if args.parallel_input and not args.source_input and not args.target_input else None
srcCorpusOut = io.open(args.source_output, encoding='utf8', mode='w') if args.source_output else None
tgtCorpusOut = io.open(args.target_output, encoding='utf8', mode='w') if args.target_output else None
pllCorpusOut = io.open(args.parallel_output, encoding='utf8', mode='w') if args.parallel_output and not args.source_output and not args.target_output else None

def WritePairIfNotTooLong(src, tgt):
  if len(src.split(' ')) > args.source_max_length or len(tgt.split(' ')) > args.target_max_length:
    return
  if pllCorpusOut:
    pllCorpusOut.write(u'{} ||| {}'.format(src, tgt))
  elif srcCorpusOut and tgtCorpusOut:
    srcCorpusOut.write(u'{}'.format(src))
    tgtCorpusOut.write(u'{}'.format(tgt))
  else:
    print 'You must provide either (parallel-output) or both (source-output and target-output)'
    exit(1)

if pllCorpusIn:
  for line in pllCorpusIn:
    src, tgt = line.split('|||')
    WritePairIfNotTooLong(src, tgt)
elif srcCorpusIn and tgtCorpusIn:
  for src, tgt in izip(srcCorpusIn, tgtCorpusIn):
    src = src.rstrip()
    WritePairIfNotTooLong(src, tgt)
else:
  print 'You must provide either (parallel-input) or both (source-input and target-input)'
  exit(1)

if srcCorpusIn: srcCorpusIn.close()
if tgtCorpusIn: tgtCorpusIn.close()
if pllCorpusIn: pllCorpusIn.close()
if srcCorpusOut: srcCorpusOut.close()
if tgtCorpusOut: tgtCorpusOut.close()
if pllCorpusOut: pllCorpusOut.close()
