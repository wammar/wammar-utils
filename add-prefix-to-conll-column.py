import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-j", "--one_based_column_number", type=int, required=True, 
                       help="the (one-based) column index to be modified.")
argparser.add_argument("-p", "--prefix", type=str, required=True, 
                       help="the string to prefix the specified column.")
args = argparser.parse_args()
column_index = args.one_based_column_number
prefix = args.prefix

with io.open(args.input_filename) as input_file, io.open(args.output_filename, mode='w') as output_file: 
  for line in input_file:
    if len(line.strip()) == 0:
      output_file.write(u'\n')
    else:
      conll_fields = line.strip().split('\t')
      conll_fields[column_index - 1] = prefix + conll_fields[column_index - 1]
      output_file.write(u'\t'.join(conll_fields) + u'\n')
