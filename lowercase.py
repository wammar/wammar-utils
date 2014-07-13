import re
import time
import io
import sys
import nltk
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-input")
argParser.add_argument("-output")
args = argParser.parse_args()

inputFile = io.open(args.input, encoding='utf8', mode='r')
outputFile = io.open(args.output, encoding='utf8', mode='w')

for line in inputFile:
  tokens = line.strip().split()
  for token in tokens:
    token = token.lower()
    outputFile.write(u'{0} '.format(token))
  outputFile.write(u'\n')
                  
inputFile.close()
outputFile.close()
