import re
import time
import io
import sys
from collections import defaultdict

ratio = sys.argv[1] # 1000:1:1
inputPrefix = sys.argv[2] # /mal2/wammar/data/morph-gen/enar/baseline/corpus.
trainPrefix = sys.argv[3] # /mal2/wammar/data/morph-gen/enar/baseline/train.
devPrefix = sys.argv[4] # /mal2/wammar/data/morph-gen/enar/baseline/dev.
testPrefix = sys.argv[5] # /mal2/wammar/data/morph-gen/enar/baseline/test.
srcExt = sys.argv[6] # en
tgtExt = sys.argv[7] # ar

srcInput = io.open(inputPrefix + srcExt, encoding='utf8', mode='r')
tgtInput = io.open(inputPrefix + tgtExt, encoding='utf8', mode='r')

srcTrain = io.open(trainPrefix + srcExt, encoding='utf8', mode='w')
tgtTrain = io.open(trainPrefix + tgtExt, encoding='utf8', mode='w')

srcDev = io.open(devPrefix + srcExt, encoding='utf8', mode='w')
tgtDev = io.open(devPrefix + tgtExt, encoding='utf8', mode='w')

srcTest = io.open(testPrefix + srcExt, encoding='utf8', mode='w')
tgtTest = io.open(testPrefix + tgtExt, encoding='utf8', mode='w')

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
