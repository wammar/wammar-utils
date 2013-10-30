import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--delimiter", type=str, default=' ||| ', help="delimiter defaults to \t")
argParser.add_argument("-1", "--firstFilename", type=str, help="src output file")
argParser.add_argument("-2", "--secondFilename", type=str, help="tgt output file")
argParser.add_argument("-i", "--inputFilename", type=str)
argParser.add_argument("-ie", "--input_encoding", type=str, default='utf8')
argParser.add_argument("-oe", "--output_encoding", type=str, default='utf8')
args = argParser.parse_args()

firstFile = io.open(args.firstFilename, encoding=args.output_encoding, mode='w')
secondFile = io.open(args.secondFilename, encoding=args.output_encoding, mode='w')
inputFile = io.open(args.inputFilename, encoding=args.input_encoding, mode='r')

counter = 0
for line in inputFile:
  splits = line.strip().split(args.delimiter)
  if len(splits) != 2: 
    continue
  firstLine, secondLine = splits
  if len(secondLine) == 0 or len(firstLine) == 0:
    print 'error: line {0} has an empty side'.format(counter)
    exit(1)
  firstFile.write(u'{0}\n'.format(firstLine.strip()))
  secondFile.write(u'{0}\n'.format(secondLine.strip()))
  counter += 1
  
firstFile.close()
secondFile.close()
inputFile.close()
