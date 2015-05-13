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
  line = line.lower()
  line = line.encode('utf8')
  outputFile.write('{}'.format(line))
                  
inputFile.close()
outputFile.close()
