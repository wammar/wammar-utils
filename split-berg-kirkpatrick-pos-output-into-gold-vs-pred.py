import re
import time
import io
import sys
from collections import defaultdict

inputFilename = sys.argv[1]
goldFilename = sys.argv[2]
predFilename = sys.argv[3]

inputFile = io.open(inputFilename, encoding='utf8', mode='r')
goldFile = io.open(goldFilename, encoding='utf8', mode='w')
predFile = io.open(predFilename, encoding='utf8', mode='w')

counter = 0
for inputLine in inputFile:
  counter += 1
  sequence = inputLine.strip().split()
  goldSequence, predictionSequence = [], []
  for item in sequence:
    [token,gold,prediction] = item.split('|')
    tokenGold = u'{0}/{1}'.format(token, gold)
    tokenPrediction = u'{0}/{1}'.format(token, prediction)
    goldSequence.append(tokenGold)
    predictionSequence.append(tokenPrediction)
  goldFile.write(u' '.join(goldSequence) + u'\n')
  predFile.write(u' '.join(predictionSequence) + u'\n')

inputFile.close()
goldFile.close()
predFile.close()
