import io
import argparse

# concatenate the first

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-j", "--first_one_based_column_number", type=int, required=True, 
                       help="the content of this column will be concatenated with the content of -k and pasted into -l.")
argparser.add_argument("-k", "--second_one_based_column_number", type=int, required=True, 
                       help="the content of -j will be concatenated with the conetnt of this column and pasted into -l.")
argparser.add_argument("-l", "--third_one_based_column_number", type=int, required=True, 
                       help="the output column, can be similar to -k or -j.")
argparser.add_argument("-s", "--separator", default=":", 
                       help="the separator to use in -l.")
args = argparser.parse_args()
first_index = args.first_one_based_column_number
second_index = args.second_one_based_column_number
third_index = args.third_one_based_column_number

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    for line in input_file:
      if len(line.strip()) == 0:
        output_file.write(u'\n')
      else:
        conll_fields = line.strip().split('\t')
        first = conll_fields[first_index - 1]
        second = conll_fields[second_index - 1]
        conll_fields[third_index - 1] = u'{}{}{}'.format(first, args.separator, second)
        output_file.write(u'\t'.join(conll_fields) + u'\n')
