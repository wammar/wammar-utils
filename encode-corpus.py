import re
import time
import io
import sys
import os
from collections import defaultdict

# splits tokens on a whitespace, and outputs unique tokens

textCorpus = io.open(sys.argv[1], encoding='utf8', mode='r')
vocabFilename = sys.argv[2]
intCorpus = io.open(sys.argv[3], encoding='utf8', mode='w')

# figures whether the vocabulary is ready
vocabReady = False
if os.path.exists(vocabFilename):
  vocabReady = True
if vocabReady:
  vocabFile = io.open(vocabFilename, encoding='utf8', mode='r')
else:
  vocabFile = io.open(vocabFilename, encoding='utf8', mode='w')

# read the vocab if ready
vocab = defaultdict(int)
if vocabReady:
  linesCounter = 0
  id = 0 # widening the scope of id
  for line in vocabFile:
    splits = line.strip().split()
    if len(splits) == 0:
      continue
    elif len(splits) != 2:
      print 'vocab file is malformatted at line #{0}'.format(linesCounter)
      exit()
    (id, token) = splits
    vocab[token] = id
    linesCounter+= 1
  nextId = int(id) + 1
else:
  # id 0 is reserved for openfst epsilon
  # id 1 is reserved for null alignments
  nextId = 2

# read the corpus
linesCounter = 0
for line in textCorpus:
  temp = []
  tokens = line.strip().split()
  for token in tokens:
    if token not in vocab.keys():
      vocab[token] = nextId
      nextId += 1
      if not vocabReady:
        vocabFile.write(u'{0} {1}\n'.format(nextId, token))
    temp.append(str(vocab[token]))
  intCorpus.write(u'{0}\n'.format(' '.join(temp)))
  # for logging only
  linesCounter += 1
  if linesCounter % 1000 == 0:
    print 'nextId={0}'.format(nextId)
    print 'linesCounter={0}'.format(linesCounter)
                  
vocabFile.close()
textCorpus.close()
intCorpus.close()
