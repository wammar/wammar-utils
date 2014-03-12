import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-d", "--delimiter", type=str, default=' ||| ', help="delimiter defaults to ' ||| '")
argParser.add_argument("-o", "--outputFilenames", nargs='+', action='append')
argParser.add_argument("-i", "--inputFilename", type=str)
argParser.add_argument("-ie", "--input_encoding", type=str, default='utf8')
argParser.add_argument("-oe", "--output_encoding", type=str, default='utf8')
argParser.add_argument("-p", "--permissive", action='store_true', help="allow the number of columns to vary from one line to another")
args = argParser.parse_args()

if args.delimiter.lower() == 'tab':
  args.delimiter = '\t'

inputFile = io.open(args.inputFilename, encoding=args.input_encoding, mode='r')
outputFiles = []
for filename in args.outputFilenames[0]:
  outputFiles.append(io.open(filename, encoding=args.output_encoding, mode='w'))

counter = 0
for line in inputFile:
  splits = line.strip().split(args.delimiter)
  if not args.permissive and len(splits) != len(outputFiles):
    print 'number of columns in line #', counter, ' is different than the number of output files specified'
    print 'columns = ', splits
    assert False
  elif args.permissive and len(splits) > len(outputFiles):
    print 'number of columns in line #', counter, ' is greater than the number of output files specified'
    print 'columns = ', splits
    assert False
  for i in xrange(len(outputFiles)):
    if len(splits) <= i:
      outputFiles[i].write(u'\n')
    else:
      outputFiles[i].write(u'{0}\n'.format(splits[i].strip()))
      if len(splits[i]) == 0 and not args.permissive:
        print 'error: line {0} has an empty column'.format(counter)
        assert False
  counter += 1
  
inputFile.close()
for output_file in outputFiles:
  output_file.close()
