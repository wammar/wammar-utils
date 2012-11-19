import re
import time
import io
import sys
import os
from collections import defaultdict

class Trie:
  def __init__(self):
    # the key that marks the end of a sequence
    self.end = ''
    # the index of the root node in the nodes list
    self.rootId = 0
    # the nodes list. each element contains a dictionary with keys
    # representing an element in the sequence and values representing
    # the next node index in the list
    self.nodes = [{self.end:('EMPTY_SEQUENCE', self.rootId)}]
    self.nextId = len(self.nodes)

  # in case you don't want any sequence to have certain IDs
  # e.g. you want to reserve the index 0 for a special kind of sequence
  def SetRoot(self, rootId):
    self.rootId = rootId
    assert(self.rootId >= 0)
    while len(self.nodes) <= self.rootId:
      self.nodes.append({self.end:('EMPTY_SEQUENCE', self.rootId)})
    self.nextId = self.rootId + 1

  # the normal scenario doesn't specify the optionalId
  # the optional id is only needed if you want to set 
  # a specific ID for some sequences (e.g. you constructed
  # a trie using data set X, and saved the IDs to file, and
  # now you want to apply the same IDs to another data set Y)
  def Index(self, sequence, optionalId = -1):
    assert(optionalId >= -1)
    self.currentId = self.rootId
    for element in sequence:
      if element not in self.nodes[self.currentId].keys():
        self.nodes[self.currentId][element] = self.nextId
        self.nodes.append({})
        self.nextId = len(self.nodes)
      self.currentId = self.nodes[self.currentId][element]
    # if an optional id is specified, override any existing ID
    if optionalId != -1:
      self.nodes[self.currentId][self.end] = (sequence, optionalId)
    # else, check whether an ID already exists. if one exists, do nothing. if no ID exist, then set self.currentId
    elif self.end not in self.nodes[self.currentId].keys():
      self.nodes[self.currentId][self.end] = (sequence, self.currentId)

    # now, we are confident this will return the sequence's ID
    return self.nodes[self.currentId][self.end][1]

  def GetAllSequenceIds(self):
    all = []
    for nodeId in range(self.rootId + 1, len(self.nodes)):
      if self.end in self.nodes[nodeId].keys():
        all.append( (self.nodes[nodeId][self.end][1], self.nodes[nodeId][self.end][0]) )
    return all

  # for debugging
  def Dump(self):
    x = -1
    for node in self.nodes:
      x += 1
      print '{0} {1}'.format(x, node)

# splits tokens on a whitespace, and outputs unique tokens

textCorpus = io.open(sys.argv[1], encoding='utf8', mode='r')
vocabFilename = sys.argv[2]
intCorpus = io.open(sys.argv[3], encoding='utf8', mode='w')
if len(sys.argv) > 4:
  vocabStatus = sys.argv[4] # to indicate the vocab file is ready, pass 'ready' here
else:
  vocabStatus = 'not ready'

# figures whether the vocabulary is ready
vocabReady = False
if vocabStatus == 'ready':
  print 'reusing the vocab file'
  vocabReady = True
else:
  print 'creating the vocab file'
if vocabReady:
  vocabFile = io.open(vocabFilename, encoding='utf8', mode='r')
else:
  vocabFile = io.open(vocabFilename, encoding='utf8', mode='w')

# read the vocab if ready
vocab = Trie()
if vocabReady:
  linesCounter = 0
  for line in vocabFile:
    splits = line.strip().split()
    if len(splits) == 0:
      continue
    elif len(splits) != 2:
      print 'vocab file is malformatted at line #{0}'.format(linesCounter)
      exit()
    (id, token) = splits
    indexedId = vocab.Index(token, int(id))
    linesCounter+= 1
else:
  # id 0 is reserved for openfst epsilon
  # id 1 is reserved for null alignments
  vocab.SetRoot(2)

# read the corpus
linesCounter = 0
for line in textCorpus:
  temp = []
  tokens = line.strip().split()
  for token in tokens:
    temp.append(str(vocab.Index(token)))
  intCorpus.write(u'{0}\n'.format(' '.join(temp)))
  # for logging only
  linesCounter += 1
  if linesCounter % 1000 == 0:
    print 'linesCounter={0}'.format(linesCounter)

if not vocabReady:
  for (wordId, word) in vocab.GetAllSequenceIds():
    vocabFile.write(u'{0} {1}\n'.format(wordId, word))
                  
vocabFile.close()
textCorpus.close()
intCorpus.close()
