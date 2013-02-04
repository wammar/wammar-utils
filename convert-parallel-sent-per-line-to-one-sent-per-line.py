import re
import time
import io
import sys
from collections import defaultdict

inputFilename = sys.argv[1] # each line in this file looks like: "source sentnece ||| tgt sentence"
outputFilename1 = inputFilename + '.src'
outputFilename2 = inputFilename + '.tgt'

inputFile = io.open(inputFilename, encoding='utf8', mode='r')
srcFile = io.open(outputFilename1, encoding='utf8', mode='w')
tgtFile = io.open(outputFilename2, encoding='utf8', mode='w')

counter = 0
for inputLine in inputFile:
  counter += 1
  [srcLine,tgtLine] = inputLine.strip().split('|||')
  srcLine = srcLine.strip() 
  tgtLine = tgtLine.strip()
  assert(len(srcLine) > 0)
  assert(len(tgtLine) > 0)
  srcFile.write(srcLine+'\n')
  tgtFile.write(tgtLine+'\n')

inputFile.close()
srcFile.close()
tgtFile.close()
