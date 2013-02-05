#!/usr/bin/python

# courtesy of Phil Blunsom

import sys
from collections import defaultdict
from math import log

def dict_max(d):
  max_val=-1
  max_key=None
  for k in d:
    if d[k] > max_val: 
      max_val = d[k]
      max_key = k
  assert max_key
  return max_key

if len(sys.argv) < 3:
  print "Usage: score-classes.py gold pred"
  exit(1)

just_tags = False
if len(sys.argv) >= 4 and sys.argv[3] == "-t":
  just_tags = True

gold_file=open(sys.argv[1],'r')
pred_file=open(sys.argv[2],'r')

gold_pred_counts = defaultdict(lambda *x: 0)
gold_counts = defaultdict(lambda *x: 0)
pred_counts = defaultdict(lambda *x: 0)
total = 0
for gold_line,pred_line in zip(gold_file,pred_file):
  gold_tokens = gold_line.split()
  pred_tokens = pred_line.split()
  assert len(gold_tokens) == len(pred_tokens)

  for gold_token,pred_token in zip(gold_tokens,pred_tokens):
    gold_term,gold_tag = gold_token.rsplit('/',1)
    pred_term,pred_tag = pred_token.rsplit('/',1)

    gold_pred_counts[gold_tag,pred_tag] += 1
    gold_counts[gold_tag] += 1
    pred_counts[pred_tag] += 1
    total += 1

ht2c = hc2t = 0.0
for (gold_tag, pred_tag), joint in gold_pred_counts.items():
    hc2t += joint / float(total) * log(pred_counts[pred_tag] / float(joint), 2.0)
    ht2c += joint / float(total) * log(gold_counts[gold_tag] / float(joint), 2.0)

ht = 0
for gold_tag, count in gold_counts.items():
    ht -= count / float(total) * log(count / float(total), 2.0)

hc = 0
for gold_tag, count in pred_counts.items():
    hc -= count / float(total) * log(count / float(total), 2.0)

h = 1 - hc2t / ht
c = 1 - ht2c / hc

print "H(T|C) %f H(C|T) %f H(T) %f H(C) %f" % (hc2t, ht2c, ht, hc),
print "where T = true, C = clusters"
print >>sys.stderr, "VMeasure = %f" % (2*h*c / (h + c))
print >>sys.stderr, "VI = %f" % (ht + hc - 2 * (ht - hc2t))
