#!/usr/bin/python

# courtesy of Phil Blunsom

import sys
from collections import defaultdict

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

gold_to_topics = defaultdict(dict)
topics_to_gold = defaultdict(dict)
term_to_topics = defaultdict(dict)

for gold_line,pred_line in zip(gold_file,pred_file):
  gold_tokens = gold_line.split()
  pred_tokens = pred_line.split()
  assert len(gold_tokens) == len(pred_tokens)

  for gold_token,pred_token in zip(gold_tokens,pred_tokens):
    gold_term,gold_tag = gold_token.rsplit('/',1)
    pred_term,pred_tag = pred_token.rsplit('/',1)

    gold_to_topics[gold_tag][pred_tag] \
      = gold_to_topics[gold_tag].get(pred_tag, 0) + 1
    term_to_topics[gold_term][pred_tag] \
      = term_to_topics[gold_term].get(pred_tag, 0) + 1
    topics_to_gold[pred_tag][gold_tag] \
      = topics_to_gold[pred_tag].get(gold_tag, 0) + 1

pred=0
correct=0
gold_file=open(sys.argv[1],'r')
pred_file=open(sys.argv[2],'r')
for gold_line,pred_line in zip(gold_file,pred_file):
  gold_tokens = gold_line.split()
  pred_tokens = pred_line.split()

  for gold_token,pred_token in zip(gold_tokens,pred_tokens):
    gold_term,gold_tag = gold_token.rsplit('/',1)
    pred_term,pred_tag = pred_token.rsplit('/',1)
    if just_tags:
      print "%s" % (pred_tag),
    else:
      print "%s/%s/%s" % (gold_token, pred_tag, dict_max(topics_to_gold[pred_tag])),
    pred += 1
    if gold_tag == dict_max(topics_to_gold[pred_tag]):
      correct += 1
  print
print >>sys.stderr, "Many-to-One Accuracy = %f" % (float(correct) / pred)
#for x in gold_to_topics: 
#  print x,dict_max(gold_to_topics[x])
#print "###################################################"
#for x in range(len(topics_to_gold)): 
#  print x,dict_max(topics_to_gold[str(x)])
#  print x,topics_to_gold[str(x)]
#print term_to_topics
