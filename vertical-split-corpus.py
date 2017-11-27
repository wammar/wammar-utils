import re
import time
import io
import sys
import argparse
from collections import defaultdict

# usage:
# corpus is assumed to consist of independent lines in a single file. lines are split deterministically into three files: train, test and dev, using the ratio specified as an argument. 

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-r", "--ratio", type=str, help="train:dev:test ratio e.g. 1000:1:1")
argParser.add_argument("-c", "--corpusFilename", type=str, help="input corpus/file")
argParser.add_argument("-t", "--trainFilename", type=str, help="output train filename")
argParser.add_argument("-d", "--devFilename", type=str, help="output dev filename")
argParser.add_argument("-s", "--testFilename", type=str, help="output test filename")
args = argParser.parse_args()

[trainSize, devSize, testSize] = args.ratio.split(':')
[trainSize, devSize, testSize] = [int(trainSize), int(devSize), int(testSize)]
cycleSize = trainSize + devSize + testSize
assert(trainSize >= 0 and devSize >= 0 and testSize >= 0 and cycleSize > 1)
corpusFile = io.open(args.corpusFilename, encoding='utf8', mode='r')
trainFile = io.open(args.trainFilename, encoding='utf8', mode='w')
testFile = io.open(args.testFilename, encoding='utf8', mode='w')
devFile = io.open(args.devFilename, encoding='utf8', mode='w')

counter = 0
for line in corpusFile:
  if trainSize != 0 and counter % cycleSize < trainSize:
    trainFile.write(line)
  elif devSize != 0 and counter % cycleSize < trainSize + devSize:
    devFile.write(line)
  elif testSize != 0 and counter % cycleSize < trainSize + devSize + testSize:
    testFile.write(line)
  else:
    print('error: something went wrong, but Im not sure what it was.')
    exit(1)   
  counter += 1

corpusFile.close()
trainFile.close()
testFile.close()
devFile.close()
