import re
import time
import io
import sys
import nltk

inputFile = io.open(sys.argv[1], encoding='utf8', mode='r')
outputFile = io.open(sys.argv[2], encoding='utf8', mode='w')

for line in inputFile:
  line = line[0].lower() + line[1:]
  tokens = line.strip().split()
  for token in tokens:
    outputFile.write(u'{0} '.format(token))
  outputFile.write(u'\n')
                  
inputFile.close()
outputFile.close()
