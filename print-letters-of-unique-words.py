import re
import time
import io
import sys
import nltk
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-s", "--split", action='store_true', help="split the word into characters when printing")
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

inputFile = io.open(args.input_filename, encoding='utf8', mode='r')
outputFile = io.open(args.output_filename, encoding='utf8', mode='w')

# find unique words
words = set()
for line in inputFile:
  tokens = line.strip().split()
  for token in tokens:
    words.add(token)

# print the letters
for word in words:
  if args.split:
    for char in word:
      outputFile.write(u'{0} '.format(char))
  else:
    outputFile.write(word)
  outputFile.write(u'\n')

inputFile.close()
outputFile.close()
