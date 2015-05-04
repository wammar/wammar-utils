import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-f", "--forward_alignments_filename", required=True)
argparser.add_argument("-b", "--backward_alignments_filename", required=True)
argparser.add_argument("-o", "--intersected_alignments_filename", required=True)
argparser.add_argument("-m", "--minimum_logprob_sum", default=-2.0, type=float)
args = argparser.parse_args()

forward = {}
intersection = defaultdict(list)

with io.open(args.forward_alignments_filename, encoding='utf8') as forward_alignments:
  for line in forward_alignments:
    src, tgt, logprob = line.strip().split(' ')
    logprob = float(logprob)
    if logprob < args.minimum_logprob_sum: continue
    forward[u'{}|||{}'.format(src, tgt)] = logprob

print 'len(forward) = ', len(forward)
  
with io.open(args.backward_alignments_filename, encoding='utf8') as backward_alignments:
  for line in backward_alignments:
    tgt, src, logprob = line.strip().split(' ')
    logprob = float(logprob)
    if logprob < args.minimum_logprob_sum: continue
    src_tgt = u'{}|||{}'.format(src, tgt)
    if src_tgt not in forward: continue
    logprob_sum = logprob + forward[src_tgt]
    if logprob_sum < args.minimum_logprob_sum: continue
    intersection[src].append( (tgt, logprob_sum,) )

print 'len(intersection)=', len(intersection)

src_counter, src_tgt_counter = 0, 0
with io.open(args.intersected_alignments_filename, encoding='utf8', mode='w') as intersected_alignments:
  for src, tgt_list in intersection.iteritems():
    src_counter += 1
    for tgt, logprob_sum in tgt_list:
      src_tgt_counter += 1
      intersected_alignments.write(u'{} {} {}\n'.format(src, tgt, logprob_sum))

print 'src_counter={}, src_tgt_counter={}'.format(src_counter, src_tgt_counter)
