import re
import time
import io
import sys
import argparse
from collections import defaultdict

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o1", "--output_source_filename")
argparser.add_argument("-o2", "--output_target_filename")
args = argparser.parse_args()

inputFilename = args.input_filename # each line in this file looks like: "source sentnece ||| tgt sentence"
outputFilename1 = args.output_source_filename
outputFilename2 = args.output_target_filename

inputFile = io.open(inputFilename, encoding='utf8', mode='r')
srcFile = io.open(outputFilename1, encoding='utf8', mode='w')
tgtFile = io.open(outputFilename2, encoding='utf8', mode='w')

counter = 0
for inputLine in inputFile:
  counter += 1
  splits = inputLine.split(' ||| ')
  if len(splits) != 2: print splits
  assert(len(splits) == 2)
  srcLine, tgtLine = splits[0].strip(), splits[1].strip()
  if len(srcLine) == 0 or len(tgtLine) == 0: continue
  assert(len(srcLine) > 0)
  assert(len(tgtLine) > 0)
  srcFile.write(srcLine+'\n')
  tgtFile.write(tgtLine+'\n')

inputFile.close()
srcFile.close()
tgtFile.close()
