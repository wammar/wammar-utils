import re
import time
import io
import sys
import nltk

_lowercase = True;
while(sys.argv[1][0] == '-'):
  if sys.argv[1][1] == 'u':
    _lowercase = False
  del sys.argv[1]
inputFile = io.open(sys.argv[1], encoding='utf8', mode='r')
outputFile = io.open(sys.argv[2], encoding='utf8', mode='w')

tokenizer = nltk.tokenize.RegexpTokenizer('\w+|\$[\d\.]+|\S+')

for line in inputFile:
  line = line.strip()
  tokens = tokenizer.tokenize(line)
  for token in tokens:
    if _lowercase:
      token = token.lower()
    outputFile.write(u'{0} '.format(token))
  outputFile.write(u'\n')
                  
inputFile.close()
outputFile.close()
