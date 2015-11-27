import io
import argparse

# converts the modified conll format of universal dependency parses to that of conll 2006. 
# the main thing is to remove multi-word annotations, and remove comment lines.
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
args = argparser.parse_args()

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    current_sentence = []
    for line in input_file:
      if len(line) > 0 and line[0] == '#':
        continue
      if len(line.strip()) == 0 and len(current_sentence) == 0:
        continue
      elif len(line.strip()) == 0 and len(current_sentence) > 0:
        output_file.write(u''.join(current_sentence) + u'\n')
        current_sentence = []
      else:
        conll_fields = line.strip().split('\t')
        # Skip lines which describe multiple words since each of the individual words has a separate line.
        if '-' in conll_fields[0]: continue
        # remove language specific extensions of dependency relationships.
        if ':' in conll_fields[7]: conll_fields[7] = conll_fields[7][:conll_fields[7].find(':')]
        # remove spaces from the second and third fields
        conll_fields[1] = conll_fields[1].replace(' ', '')
        conll_fields[2] = conll_fields[1].replace(' ', '')
        line = u'\t'.join(conll_fields)+u'\n'
        current_sentence.append(line)

    # consumed all lines in input file
    if len(current_sentence) > 0:
      output_file.write(u''.join(current_sentence) + u'\n')
      current_sentence = []
