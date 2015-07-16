import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict
import math

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-if", "--forward-params", help="(required) parameters of forward alignment with fast_align")
argparser.add_argument("-ir", "--reverse-params", default="", 
                       help="(optional) parameters of reverse alignment with fast_align")
argparser.add_argument("-t", "--threshold", type=float, default=0.1, help="the min allowed p(x|y) parameter")
argparser.add_argument("-d", "--output-dictionary", help="(required) output dictionary")
args = argparser.parse_args()

# open files
forward = gzip.open(args.forward_params, mode='r') if args.forward_params.endswith('.gz') else open(args.forward_params, mode='r')
reverse = None if len(args.reverse_params) == 0 else (gzip.open(args.reverse_params, mode='r') if args.reverse_params.endswith('.gz') else open(args.reverse_params, mode='r'))
dictionary = gzip.open(args.output_dictionary, mode='w') if args.output_dictionary.endswith('.gz') else open(args.output_dictionary, mode='w')

tgt2src = defaultdict(set)
for line in forward:
  # read forward parameter
  line = line.decode('utf8')
  splits = line.strip().split('\t')
  if len(splits) != 3: 
    print "the line:", line, "in", args.forward_params, "does is malformatted"
    exit(1)
  src, tgt, logprob = splits
  logprob = float(logprob)

  # skip null alignments
  if src == '<eps>' or tgt == '<eps>': continue

  # skip parameter values less than specified threshold
  if logprob < math.log(args.threshold): continue

  # add pair to the dictionary
  tgt2src[tgt].add(src)

dictionary_entries_count = 0

if reverse:
  for line in reverse:
    # read reverse parameter
    line = line.decode('utf8')
    splits = line.strip().split('\t')
    if len(splits) != 3: 
      print "line:", line, "in", args.reverse_params, "is malformatted."
      exit(1)
    tgt, src, logprob = splits
    logprob = float(logprob)

    # discard reverse parameters which do not have a counterpart among the
    # filtered forward parameters
    if tgt not in tgt2src or src not in tgt2src[tgt]:
      continue

    # skip parameter values less than specified threhsold 
    if logprob < math.log(args.threshold): continue

    # src/tgt pairs which survived all previous skipping are added to the
    # filtered dictionary
    output_line = u'{} ||| {}\n'.format(src, tgt)
    output_line = output_line.encode('utf8')
    dictionary.write(output_line)
    dictionary_entries_count += 1

# when reverse params are not specified, write all pairs in the collection
# to the output dictionary
else: 
  for tgt in tgt2src.keys():
    for src in tgt2src[tgt]:
      output_line = u'{} ||| {}\n'.format(src, tgt)
      output_line = output_line.encode('utf8')
      dictionary.write(output_line)
      dictionary_entries_count += 1

dictionary.close()
forward.close()
if reverse: reverse.close()

print '{} (src,tgt) pairs written to {}'.format(dictionary_entries_count, args.output_dictionary)
