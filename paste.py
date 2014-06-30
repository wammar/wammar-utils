import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--delimiter", default='\t', help="delimiter defaults to \t")
argparser.add_argument("-i", "--input_filenames", nargs='+', action='append')
argparser.add_argument("-o", "--output_filename")
argparser.add_argument("-ie", "--input_encoding", default='utf8')
argparser.add_argument("-oe", "--output_encoding", default='utf8')
argparser.add_argument("-p", "--permissive", action='store_true', help="allow empty columns")
args = argparser.parse_args()

if args.delimiter.lower() == 'tab':
  args.delimiter = '\t'

inputFiles = []
for filename in args.input_filenames[0]:
  inputFiles.append(io.open(filename, encoding=args.input_encoding, mode='r'))
outputFile = io.open(args.output_filename, encoding=args.output_encoding, mode='w')

counter = -1
while True:
  counter += 1
  inputLines = []
  eof = False
  for i in range(0, len(inputFiles)):
    line = inputFiles[i].readline()
    if not line and i == 0: 
      eof = True
      break
    inputLines.append(line.strip())
    if not line: 
      print 'warning: input file #{} has fewer lines than file #0'.format(i)
    elif not line.strip(): 
      print 'warning: input file #{1} has empty line at {0}'.format(counter, i)
  if eof: 
    break
  outputFile.write(args.delimiter.join(inputLines) + u'\n')

for f in inputFiles:
  f.close()
outputFile.close()

print '{} lines written'.format(counter)
