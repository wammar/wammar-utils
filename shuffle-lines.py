import random
import sys
import argparse

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

with open(args.input_filename,'r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()
with open(args.output_filename,'w') as target:
    for _, line in data:
        target.write( line )
