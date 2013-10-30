import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--delimiter", default='\t', help="delimiter defaults to \t")
argParser.add_argument("-1", "--firstFilename")
argParser.add_argument("-2", "--secondFilename")
argParser.add_argument("-3", "--thirdFilename", default='')
argParser.add_argument("-o", "--outputFilename")
argParser.add_argument("-ie", "--input_encoding", default='utf8')
argParser.add_argument("-oe", "--output_encoding", default='utf8')
args = argParser.parse_args()

firstFile = io.open(args.firstFilename, encoding=args.input_encoding, mode='r')
secondFile = io.open(args.secondFilename, encoding=args.input_encoding, mode='r')
thirdFile = io.open(args.thirdFilename, encoding=args.input_encoding, mode='r') if len(args.thirdFilename) > 0 else None
outputFile = io.open(args.outputFilename, encoding=args.output_encoding, mode='w')

counter = 0
for firstLine in firstFile:
  secondLine = secondFile.readline()
  if thirdFile:
    thirdLine = thirdFile.readline()
  if len(secondLine) == 0:
    print 'error: second file is shorter than first file at line {0}'.format(counter)
    exit(1)
  elif thirdFile and len(thirdLine) == 0:
    print 'error: third file is shorter than first file at line {0}'.format(counter)
    exit(1)
  outputFile.write(u'{0}'.format(firstLine.strip()))
  outputFile.write(u'{0}{1}'.format(args.delimiter, secondLine.strip()))
  if thirdFile:
    outputFile.write(u'{0}{1}'.format(args.delimiter, thirdLine.strip()))
  outputFile.write(u'\n')
  counter += 1
  
firstFile.close()
secondFile.close()
outputFile.close()
