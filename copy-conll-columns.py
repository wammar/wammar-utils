import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-f", type=int, required=True, 
                       help="one-based index of the column to be copied.")
argparser.add_argument("-t", type=int, required=True, 
                       help="one-based index of the column to be overwritten.")
args = argparser.parse_args()
from_index = args.f
to_index = args.t

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    for line in input_file:
      if len(line.strip()) == 0:
        output_file.write(u'\n')
      else:
        conll_fields = line.strip().split('\t')
        conll_fields[to_index - 1] = conll_fields[from_index - 1]
        output_file.write(u'\t'.join(conll_fields) + u'\n')
