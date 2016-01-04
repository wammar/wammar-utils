import re
import time
import io
import sys
import argparse
from collections import defaultdict
from random import shuffle
import shutil
import os

# usage:
# corpus consists of a bunch of files in a flat directory. this script will split the files according to the specified ratios into train/dev/test directories.

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-r", "--ratio", type=str, help="train:dev:test ratio e.g. 1000:1:1")
argParser.add_argument("-c", "--corpus_dir", type=str, help="input corpus directory")
argParser.add_argument("-t", "--train_dir", type=str, help="output train directory")
argParser.add_argument("-d", "--dev_dir", type=str, help="output dev directory")
argParser.add_argument("-s", "--test_dir", type=str, help="output test directory")
args = argParser.parse_args()

[trainSize, devSize, testSize] = args.ratio.split(':')
[trainSize, devSize, testSize] = [int(trainSize), int(devSize), int(testSize)]
cycleSize = trainSize + devSize + testSize
assert(trainSize >= 0 and devSize >= 0 and testSize >= 0 and cycleSize > 1)

# get a list of all files in the corpus directory
corpus_filenames = os.listdir(args.corpus_dir)
shuffle(corpus_filenames)

# copy files to splits, assume the directories are already created
counter = 0
for filename in corpus_filenames:
  original_path = os.path.join(args.corpus_dir, filename)
  if trainSize != 0 and counter % cycleSize < trainSize:
    new_path = os.path.join(args.train_dir, filename)
  elif devSize != 0 and counter % cycleSize < trainSize + devSize:
    new_path = os.path.join(args.dev_dir, filename)
  elif testSize != 0 and counter % cycleSize < trainSize + devSize + testSize:
    new_path = os.path.join(args.test_dir, filename)
  else:
    print 'error: something went wrong, but Im not sure what it was.'
    exit(1)   
  shutil.copy(original_path, new_path)
  counter += 1

