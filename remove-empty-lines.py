import io
import argparse

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename")
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for line in input_file:
    if len(line.strip()) > 0:
      output_file.write(line)

