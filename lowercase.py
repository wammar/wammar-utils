import re
import time
import io
import sys
import nltk
import argparse
import gzip

argParser = argparse.ArgumentParser()
argParser.add_argument("-input")
argParser.add_argument("-output")
args = argParser.parse_args()

inputFile = gzip.open(args.input, mode='r') if args.input.endswith('.gz') else open(args.input, mode='r')
outputFile = gzip.open(args.output, mode='w') if args.output.endswith('.gz') else open(args.output, mode='w')

for line in inputFile:
  line = line.decode('utf8')
  tokens = line.strip().split()
  for i in xrange(len(tokens)):
    tokens[i] = tokens[i].lower()
    token = tokens[i].encode('utf8')
    outputFile.write('{}{}'.format(token, ' ' if i < len(tokens)-1 else ''))
  outputFile.write('\n')
                  
inputFile.close()
outputFile.close()
