import re
import time
import io
import sys
import nltk

inputFile = io.open(sys.argv[1], encoding='utf8', mode='r')
outputFile = io.open(sys.argv[2], encoding='utf8', mode='w')

for line in inputFile:
  for letter in line.strip().lower():
    cluster = 'c'
    if letter in 'aeiouyw':
      cluster = 'v'
    elif letter == ' ':
      cluster = ' '
    outputFile.write(u'{0}'.format(cluster))
  outputFile.write(u'\n')

inputFile.close()
outputFile.close()
