import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input-filename", required=True, help="Example input: https://raw.githubusercontent.com/jiangfeng1124/acl15-clnndep/master/resources/align/fr-en.align")
argparser.add_argument("-o", "--output-filename", required=True)
argparser.add_argument("-max", "--max-targets-per-source", type=int, default=3)
argparser.add_argument("-min", "--min-alignment-frequency", type=int, default=10)
argparser.add_argument("-k", "--ignore-k-ambiguous-words", type=int, default=100)
args = argparser.parse_args()

with gzip.open(args.output_filename, mode='w') if args.output_filename.endswith('.gz') else open(args.output_filename, mode='w') as output_file, gzip.open(args.input_filename, mode='r') if args.input_filename.endswith('.gz') else open(args.input_filename, mode='r') as input_file:

  # in the first pass, build a reverse map from tgt word to src words
  tgt_to_srcs = defaultdict(set)
  for in_line in input_file:
    in_line = in_line.decode('utf8').strip()
    splits = in_line.split(' ||| ')
    assert(len(splits) == 2)
    src, tgts = splits[0], splits[1]
    tgts = tgts.split(' ')
    # for each translation
    for i in xrange(len(tgts)):
      tgt_splits = tgts[i].split('__')
      tgt, frequency = tgt_splits[0], int(tgt_splits[1])
      tgt_to_srcs[tgt].add(src)

  input_file = gzip.open(args.input_filename, mode='r') if args.input_filename.endswith('.gz') else open(args.input_filename, mode='r')
  for in_line in input_file:
    in_line = in_line.decode('utf8').strip()
    splits = in_line.split(' ||| ')
    assert(len(splits) == 2)
    src, tgts = splits[0], splits[1]
    tgts = tgts.split(' ')
    # ignore ambiguous source words which are aligned to more than K translations.
    if len(tgts) > args.ignore_k_ambiguous_words: continue
    # for each translation
    for i in xrange(len(tgts)):
      # only consider the most frequent targets.
      # here, we assume translations are sorted such that more frequent alignments appear first.
      if i >= args.max_targets_per_source: continue
      tgt_splits = tgts[i].split('__')
      # this condition means that the target word itself contains the string "__". We ignore such translations.
      if len(tgt_splits) > 2: continue
      tgt, frequency = tgt_splits[0], int(tgt_splits[1])
      # ignore ambiguous tgt words which are aligned to more than K source words.
      if len(tgt_to_srcs[tgt]) > args.ignore_k_ambiguous_words: continue
      # ignore infrequent translations
      if frequency < args.min_alignment_frequency: continue
      # write this translation in a separate line in the output file
      out_line = u'{} ||| {}\n'.format(src, tgt)
      output_file.write(out_line.encode('utf8'))
