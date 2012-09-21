import re
import time
import io
import sys
from collections import defaultdict

srcCorpusIn = io.open(sys.argv[1], encoding='utf8', mode='r')
tgtCorpusIn = io.open(sys.argv[2], encoding='utf8', mode='r')
srcCorpusOut = io.open(sys.argv[3], encoding='utf8', mode='w')
tgtCorpusOut = io.open(sys.argv[4], encoding='utf8', mode='w')
srcMaxLength = int(sys.argv[5])
tgtMaxLength = int(sys.argv[6])

for srcLine in srcCorpusIn:
  tgtLine = tgtCorpusIn.readline()
  srcCount = len(srcLine.split())
  tgtCount = len(tgtLine.split())
  if srcCount > srcMaxLength or tgtCount > tgtMaxLength:
    continue
  srcCorpusOut.write(srcLine)
  tgtCorpusOut.write(tgtLine)
  
srcCorpusIn.close()
tgtCorpusIn.close()
srcCorpusOut.close()
tgtCorpusOut.close()
