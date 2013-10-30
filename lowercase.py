import re
import time
import io
import sys
import nltk
import argparse

argParser = argparse.ArgumentParser()
argParser.add_argument("-input")
argParser.add_argument("-output")
argParser.add_argument("-ie", "--input_encoding", type=str, default='utf8')
argParser.add_argument("-oe", "--output_encoding", type=str, default='utf8')
args = argParser.parse_args()

inputFile = io.open(args.input, encoding=args.input_encoding, mode='r')
outputFile = io.open(args.output, encoding=args.output_encoding, mode='w')

for line in inputFile:
  tokens = line.strip().split()
  for token in tokens:
    token = token.lower()
    outputFile.write(u'{0} '.format(token))
  outputFile.write(u'\n')
                  
inputFile.close()
outputFile.close()
