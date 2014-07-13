import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True, help="conll 2007 format")
argparser.add_argument("-o", "--output_filename", required=True, help="conll 2007 format")
args = argparser.parse_args()

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    prev_fields = None
    for line in input_file:
      if len(line.strip()) == 0:
        prev_fields[6] = u'0'
        output_file.write(u'\t'.join(prev_fields) + u'\n')
        prev_fields = []
      else:
        if prev_fields != None:
          output_file.write(u'\t'.join(prev_fields) + u'\n')
        prev_fields = line.strip().split('\t')
        prev_fields[6] = u'{}'.format(int(prev_fields[0]) + 1)
    output_file.write(u'\t'.join(prev_fields) + u'\n')
