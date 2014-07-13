import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i1", "--input1_filename")
argparser.add_argument("-i2", "--input2_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

input1_lines = io.open(args.input1_filename, encoding='utf8').readlines()
input2_lines = io.open(args.input2_filename, encoding='utf8').readlines()

if len(input1_lines) != len(input2_lines):
  with open(args.output_filename, mode='w') as output_file:
    output_file.write('ERROR: number of lines in ' + str(args.input1_filename), ' is different than in ', str(args.input2_filename), ': ', str(len(input1_lines)), ' vs. ', str(len(input2_lines)) + '\n')
  exit(1)

total, correct = 0, 0
confusion = defaultdict(lambda: defaultdict(int))
input1_labels, input2_labels = set(), set()
for line_id in range(0, len(input1_lines)):
  line1_labels = input1_lines[line_id].strip().split()
  line2_labels = input2_lines[line_id].strip().split()
  if len(line1_labels) != len(line2_labels):
    with open(args.output_filename, mode='w') as output_file:
      output_file.write('ERROR: number of labels in line #' + str(line_id) + ' of ' + args.input1_filename + ' is different than in ' + args.input2_filename + '\n')
    exit(1)
  
  for position in range(0, len(line1_labels)):
    label1, label2 = line1_labels[position], line2_labels[position]
    input1_labels.add(label1)
    input2_labels.add(label2)
    total += 1
    if label1 == label2:
      correct += 1
    confusion[label1][label2] += 1
  
with open(args.output_filename, mode='w') as output_file:
  output_file.write('accuracy = ' + str(correct) + '/' + str(total) + ' = ' + str(round(1.0 * correct / total, 2)) + ' (out of 1.0)\n')
  # write headers line of all labels in input1
  output_file.write('\ni2\\i1\t')
  for label1 in input1_labels: 
    output_file.write(str(label1) + '\t')
  output_file.write('\n')
  # write a line for each label in input2
  for label2 in input2_labels:
    output_file.write(str(label2) + '\t')
    for label1 in input1_labels:
      output_file.write(str(confusion[label1][label2]) + '\t')
    output_file.write('\n')

