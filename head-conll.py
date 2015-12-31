import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-n", "--number_of_sentences", type=int, required=True, 
                       help="maximum number of sentences in the output file.")
args = argparser.parse_args()

with io.open(args.input_filename) as input_file, io.open(args.output_filename, mode='w') as output_file: 
  sentences_counter = 0
  for line in input_file:
    if line[0] == '#':
      continue
    elif len(line.strip()) == 0:
      output_file.write(u'\n')
      sentences_counter += 1
      if sentences_counter == args.number_of_sentences: break
    else:
      output_file.write(line)
