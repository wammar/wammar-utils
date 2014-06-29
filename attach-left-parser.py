import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True, help="conll 2007 format")
argparser.add_argument("-o", "--output_filename", required=True, help="conll 2007 format")
args = argparser.parse_args()

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    parent=0
    for line in input_file:
      if len(line.strip()) == 0:
        output_file.write(u'\n')
        parent=0
      else:
        conll_fields = line.strip().split('\t')
        conll_fields[6] = u'{}'.format(parent)
        parent += 1
        output_file.write(u'\t'.join(conll_fields))
        output_file.write(u'\n')
