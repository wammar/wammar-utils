import re
import time
import io
import sys
import nltk

inputFile = io.open(sys.argv[1], encoding='utf8', mode='r')
outputFile = io.open(sys.argv[2], encoding='utf8', mode='w')

allowDigits = False;

# find unique words
words = set()
for line in inputFile:
  words = line.strip().split()
  # print the letters
  for word in words:
    # look for non-latin characters
    valid = False
    if allowDigits:
      if re.search(u'[^a-zA-Z0-9]', word) == None:
        valid = True
    else:
      if re.search(u'[^a-zA-Z]', word) == None:
        valid = True
      
    # skip invalid words
    if not valid:
      continue

    # print valid words only
    outputFile.write(word + ' ')
  # newline
  outputFile.write(u'\n')
                  
inputFile.close()
outputFile.close()
