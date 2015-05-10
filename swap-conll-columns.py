import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-j", "--first_one_based_column_number", type=int, required=True, 
                       help="one of the two column indexes to be swapped (one-based index).")
argparser.add_argument("-k", "--second_one_based_column_number", type=int, required=True, 
                       help="one of the two column indexes to be swapped (one-based index).")
args = argparser.parse_args()
first_index = args.first_one_based_column_number
second_index = args.second_one_based_column_number

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    for line in input_file:
      if len(line.strip()) == 0:
        output_file.write(u'\n')
      else:
        conll_fields = line.strip().split('\t')
        temp = conll_fields[first_index - 1]
        conll_fields[first_index - 1] = conll_fields[second_index - 1]
        conll_fields[second_index - 1] = temp
        output_file.write(u'\t'.join(conll_fields) + u'\n')
