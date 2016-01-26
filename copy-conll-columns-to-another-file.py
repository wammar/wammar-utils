import io
import argparse

# concatenate the first

argparser = argparse.ArgumentParser()
argparser.add_argument("-i1", "--input1_filename", required=True)
argparser.add_argument("-i2", "--input2_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-j", "--first_one_based_column_number", type=int, required=True, 
                       help="the content of this column will be copied from input1.")
argparser.add_argument("-k", "--second_one_based_column_number", type=int, required=True, 
                       help="input2 will be copied to the output, except this column which will be replaced with the -j column from input1.")
args = argparser.parse_args()
first_index = args.first_one_based_column_number
second_index = args.second_one_based_column_number

with io.open(args.input1_filename) as input1_file, io.open(args.input2_filename) as input2_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    for line1, line2 in zip(input1_file, input2_file):
      if min(len(line1), len(line2)) == 0 and max(len(line1), len(line2)) > 0:
        print "the two input conll files do not correspond to the same text."
        assert False
      if len(line2.strip()) == 0:
        output_file.write(u'\n')
      else:
        conll1_fields, conll2_fields = line1.strip().split('\t'), line2.strip().split('\t')
        conll2_fields[second_index - 1] = conll1_fields[first_index - 1]
        output_file.write(u'\t'.join(conll2_fields) + u'\n')
