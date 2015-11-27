import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-c", "--one_based_column_number", type=int, default=2)
args = argparser.parse_args()

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    for line in input_file:
      if len(line.strip()) == 0:
        output_file.write(u'\n')
      else:
        conll_fields = line.strip().split('\t')
        # Skip lines which describe multiple words since each of the individual words has a separate line. 
        if '-' in conll_fields[0]: continue
        if conll_fields[0][0] == '#': continue
        output_file.write(conll_fields[args.one_based_column_number-1])
        output_file.write(u' ')
        
