import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-ratio", "--ratio", type=str, help="train:dev:test ratio e.g. 1000:1:1")
argParser.add_argument("-corpus-src", "--corpusSrcFilename", type=str, help="input corpus file (src side)")
argParser.add_argument("-corpus-tgt", "--corpusTgtFilename", type=str, help="input corpus file (tgt side)")
argParser.add_argument("-train-src", "--trainSrcFilename", type=str, help="output train filename (src side)")
argParser.add_argument("-train-tgt", "--trainTgtFilename", type=str, help="output train filename (tgt side)")
argParser.add_argument("-dev-src", "--devSrcFilename", type=str, help="output dev filename (src side)")
argParser.add_argument("-dev-tgt", "--devTgtFilename", type=str, help="output dev filename (tgt side)")
argParser.add_argument("-test-src", "--testSrcFilename", type=str, help="output test filename (src side)")
argParser.add_argument("-test-tgt", "--testTgtFilename", type=str, help="output test filename (tgt side)")
args = argParser.parse_args()

ratio = args.ratio # 1000:1:1

srcInput = io.open(args.corpusSrcFilename, encoding='utf8', mode='r')
tgtInput = io.open(args.corpusTgtFilename, encoding='utf8', mode='r')

srcTrain = io.open(args.trainSrcFilename, encoding='utf8', mode='w')
tgtTrain = io.open(args.trainTgtFilename, encoding='utf8', mode='w')

srcDev = io.open(args.devSrcFilename, encoding='utf8', mode='w')
tgtDev = io.open(args.devTgtFilename, encoding='utf8', mode='w')

srcTest = io.open(args.testSrcFilename, encoding='utf8', mode='w')
tgtTest = io.open(args.testTgtFilename, encoding='utf8', mode='w')

[trainSize, devSize, testSize] = ratio.split(':')
[trainSize, devSize, testSize] = [int(trainSize), int(devSize), int(testSize)]

counter = 0
for srcLine in srcInput:
  tgtLine = tgtInput.readline()
  counter += 1
  if counter <= trainSize:
    srcTrain.write(srcLine)
    tgtTrain.write(tgtLine)
  elif counter <= trainSize + devSize:
    srcDev.write(srcLine)
    tgtDev.write(tgtLine)
  elif counter < trainSize + devSize + testSize:
    srcTest.write(srcLine)
    tgtTest.write(tgtLine)
  elif counter == trainSize + devSize + testSize:
    srcTest.write(srcLine)
    tgtTest.write(tgtLine)
    counter = 0
  else:
    print 'error: sizes don\'t make sense'
    exit(1)   

srcInput.close()
tgtInput.close()
srcTrain.close()
tgtTrain.close()
srcDev.close()
tgtDev.close()
srcTest.close()
tgtTest.close()
