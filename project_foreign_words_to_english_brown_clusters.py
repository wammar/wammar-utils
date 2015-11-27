import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()

# TODO(wammar): implement the "robust projection" methods of Guo et al. (ACL 2015), which assigns "OOV" foreign words to the cluster of edit-1-distant words.
argparser.add_argument("-ib", "--input-english-brown-clusters", help="input english brown clusters")
argparser.add_argument("-ob", "--output-foreign-brown-clusters", help="output foreign brown clusters")
argparser.add_argument("-ia", "--input-alignment-probs", help="input alignment probabilities, each line is formatted: foreign_word english_word p(english_word|foregin_word)")
args = argparser.parse_args()

# read brown clusters
english_to_cluster = {}
with io.open(args.input_english_brown_clusters, encoding='utf8') as english_clusters:
  for line in english_clusters:
    # each line consists of three tab-delimited fields: brown cluster, english word, frequency
    splits = line.split('\t')
    if len(splits) != 3: 
      print 'the following line in the clusters file is malformatted', line
      exit
    cluster, english, frequency = splits[0], splits[1], splits[2]
    english_to_cluster[english] = cluster

# read word alignment probabilities
alignments = defaultdict(lambda: defaultdict(float))
with io.open(args.input_alignment_probs, encoding='utf8') as alignments_file:
  for line in alignments_file:
    # each line consists of three space-delimited fields: foregin word, english word, alignment probability
    splits = line.strip().split()
    if (len(splits) != 3): 
      print 'the following line in the alignments file is malformatted', line
      exit
    foreign, english, prob = splits[0], splits[1], float(splits[2])
    alignments[foreign][english] = prob

# for each foreign word, write the brown cluster of the most likely english translation (for which we have a brown cluster)
with io.open(args.output_foreign_brown_clusters, encoding='utf8', mode='w') as output_file:
  for foreign in alignments.keys():
    best_cluster = ''
    best_prob = 0.0
    for english, prob in alignments[foreign].items():
      # skip english translatiosn for which we don't have an assigned cluster
      if english not in english_to_cluster: continue
      # skip english translations which are less likely than what we already used
      if prob < best_prob: continue
      # if you reach this far, update best_cluster and best_prob
      best_cluster, best_prob = english_to_cluster[english], prob
    # skip foreign words we can't project
    if len(best_cluster) == 0: continue
    # write the projected cluster of this foreign word, with made-up freq of 10
    output_file.write(u'{}\t{}\t{}\n'.format(best_cluster, foreign, 10))
