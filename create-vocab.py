import re
import time
import io
import sys
from collections import defaultdict

# splits tokens on a whitespace, and outputs unique tokens

tokenizedCorpus = io.open(sys.argv[1], encoding='utf8', mode='r')
vocabFile = io.open(sys.argv[2], encoding='utf8', mode='w')

vocab = defaultdict(int)
for line in tokenizedCorpus:
  tokens = line.strip().split()
  for token in tokens:
    vocab[token] += 1

counter = 0
for key in vocab.keys():
  vocabFile.write(u'{0} {1} {2}\n'.format(counter, key, vocab[key]))
  counter += 1

tokenizedCorpus.close()
vocabFile.close()
