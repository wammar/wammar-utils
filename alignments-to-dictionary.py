import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict
from itertools import izip

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-ip", "--input_parallel", required=True)
argparser.add_argument("-ia", "--input_alignments", required=True)
argparser.add_argument("-of", "--output_forward_dictionary", required=True)
argparser.add_argument("-ob", "--output_backward_dictionary", required=True)
argparser.add_argument("-op", "--output_product_dictionary", required=True)
args = argparser.parse_args()

# open input files
input_parallel_file, input_alignments_file = open(args.input_parallel, mode='r'), open(args.input_alignments, mode='r')

# initialize dictionaries
forward_dict, backward_dict = defaultdict(lambda: defaultdict(float)), defaultdict(lambda: defaultdict(float))

# read one sentence pair at a time
sentence_pairs_count = -1
for sentence_pair_line, alignments_line in izip(input_parallel_file, input_alignments_file):

  # read the source and target tokens of this sentence pair
  sentence_pairs_count += 1
  sentence_pair_line, alignments_line = sentence_pair_line.decode('utf8').rstrip(), alignments_line.decode('utf8').rstrip()
  source_line, target_line = sentence_pair_line.split(" ||| ")
  source_tokens, target_tokens = source_line.split(' '), target_line.split(' ')
  
  # read the translationally-equivalent word pairs according to alignments
  if len(alignments_line.strip()) == 0: continue
  word_pair_indexes = [tuple(x.split('-')) for x in alignments_line.split(' ')]
  word_pairs = [ (source_tokens[int(source_index)], target_tokens[int(target_index)],) for (source_index, target_index,) in word_pair_indexes ]
  #print word_pairs

  # update the forward and backward dictionary
  for (source_token, target_token) in word_pairs:
    forward_dict[source_token][target_token] += 1
    backward_dict[target_token][source_token] += 1

# close input files
input_parallel_file.close(); input_alignments_file.close();

# write forward dictionary
with open(args.output_forward_dictionary, mode='w') as forward_file:
  for source_word in forward_dict.keys():
    normalizer = sum(forward_dict[source_word].values())
    for target_word, alignments_count in forward_dict[source_word].viewitems():
      prob = 1.0 * alignments_count / normalizer
      forward_dict[source_word][target_word] = prob
      if alignments_count == 1: continue
      forward_file.write(u'{} {} {}\n'.format(source_word, target_word, prob).encode('utf8'))

# write backward dictionary
with open(args.output_backward_dictionary, mode='w') as backward_file:
  for target_word in backward_dict.keys():
    normalizer = sum(backward_dict[target_word].values())
    for source_word, alignments_count in backward_dict[target_word].viewitems():
      prob = 1.0 * alignments_count / normalizer
      backward_dict[target_word][source_word] = prob
      if alignments_count == 1: continue
      backward_file.write(u'{} {} {}\n'.format(target_word, source_word, prob).encode('utf8'))

# write product dictionary (i.e., forward probability * backward probability)
with open(args.output_product_dictionary, mode='w') as product_file:
  for source_word in forward_dict.keys():
    for target_word, forward_prob in forward_dict[source_word].viewitems():
      product = forward_prob * backward_dict[target_word][source_word]
      product_file.write(u'{} {} {}\n'.format(source_word, target_word, product).encode('utf8'))
