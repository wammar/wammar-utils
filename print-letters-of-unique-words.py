import re
import time
import io
import sys
import nltk

inputFile = io.open(sys.argv[1], encoding='utf8', mode='r')
outputFile = io.open(sys.argv[2], encoding='utf8', mode='w')

# find unique words
words = set()
for line in inputFile:
  tokens = line.strip().split()
  for token in tokens:
    words.add(token)

# print the letters
for word in words:
  for char in word:
    outputFile.write(u'{0} '.format(char))
  outputFile.write(u'\n')
                  
inputFile.close()
outputFile.close()
