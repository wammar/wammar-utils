import io
import argparse

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-d", "--delimiter", default="_")
argparser.add_argument("-c", "--columns", default="2,5", help="comma-delimited list of column numbers (one-based) to be copy for each token to the output file.")
args = argparser.parse_args()

columns = args.columns.split(',')
columns = [int(column)-1 for column in columns]

with io.open(args.input_filename, encoding='utf8') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  tokens = []
  for in_line in input_file:
    
    # is this the end of a sentence?
    in_line = in_line.strip()
    if len(in_line) == 0:
      if len(tokens):
        output_file.write(' '.join(tokens) + u'\n')
      tokens = []
      continue

    # parse conll line
    fields = in_line.split('\t')
    selected_fields = [fields[column] for column in columns]
    for selected_field in selected_fields:
      if args.delimiter in selected_field:
        print 'WARNING: one of the selected fields "' + selected_field + '" already contains the designated delimiter "' + args.delimiter + '"'
    token = args.delimiter.join(selected_fields)
    tokens.append(token)

# writ the last sentence
if len(tokens):
  output_file.write(' '.join(tokens) + u'\n')
