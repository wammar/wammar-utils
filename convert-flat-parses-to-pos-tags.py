import re
import time
import io
import sys
import nltk
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-i", help="input flat parses (depth = 1). one sentence per line.")
argParser.add_argument("-ot", help="output tokens. one sentence per line.")
argParser.add_argument("-op", help="output part-of-speech tags. one sentence per line.")
args = argParser.parse_args()

inputFile = io.open(args.i, encoding='utf8', mode='r')
outputTokensFile = io.open(args.ot, encoding='utf8', mode='w')
outputTagsFile = io.open(args.op, encoding='utf8', mode='w')

lines_counter = 0
for line in inputFile:
  lines_counter += 1
  if not line.startswith(u'(TOP (S ('):
    print u'WARNING: skipping line #', lines_counter, ' which does not start with the prefix "(TOP (S (":'
    print line
    continue
  line = line[9:-6]
  token_tag_pairs = line.split(u') (')
  tokens, tags = [], []
  for token_tag_pair in token_tag_pairs:
    token, tag = token_tag_pair.split(u' ')
    tokens.append(token)
    tags.append(tag)

  outputTokensFile.write(u'{}\n'.format(u' '.join(tokens)))
  outputTagsFile.write(u'{}\n'.format(u' '.join(tags)))
                  
inputFile.close()
outputTokensFile.close()
outputTagsFile.close()
