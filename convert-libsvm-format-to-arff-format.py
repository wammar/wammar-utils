import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

# scan the input (libsvm) file so that we can write the header file
all_feature_ids, all_class_labels = set(), set()
with open(args.input_filename) as input_file:
  # read the libsvm formatted file
  lines_read = 0
  for line in input_file:
    splits = line.split()
    label, splits = splits[0], splits[1:]
    features = {}
    all_class_labels.add(label)
    for i in range(len(splits)):
      feature_id, feature_value = splits[i].split(':')
      features[feature_id] = feature_value
      all_feature_ids.add(feature_id)
    lines_read += 1
    if lines_read % 1000 == 0:
      print 'lines_read = {}'.format(lines_read)
print 'all_feature_ids = {}'.format(' '.join(all_feature_ids))
print 'all_class_labels = {}'.format(' '.join(all_class_labels))

with open(args.output_filename, 'w') as output_file, open(args.input_filename) as input_file:
  # write arff header
  output_file.write('@RELATION {}\n'.format(args.input_filename))
  for feature_id in all_feature_ids:
    output_file.write('@ATTRIBUTE a{} REAL\n'.format(feature_id))
  output_file.write('@ATTRIBUTE class {}{}{}\n'.format('{', ','.join(all_class_labels), '}'))
  output_file.write('@DATA\n')

  # read libsvm file and write arff file, line by line
  examples_written = 0
  for line in input_file:
    # parse input line into label, features
    splits = line.split()
    label, splits = splits[0], splits[1:]
    features = {}
    all_class_labels.add(label)
    for i in range(len(splits)):
      feature_id, feature_value = splits[i].split(':')
      features[feature_id] = feature_value
      all_feature_ids.add(feature_id)
    # format output line
    for feature_id in all_feature_ids:
      feature_value = features[feature_id] if feature_id in features else 0.0
      output_file.write('{},'.format(feature_value))
      output_file.write(label)
    output_file.write('\n')
    if examples_written % 1000 == 0:
      print 'examples_written = {}'.format(examples_written)
    examples_written += 1
print 'finished writing {} lines'.format(examples_written)
