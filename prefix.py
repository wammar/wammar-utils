import io
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-p", "--prefix", type=str, required=True, 
                       help="the string to prefix lines.")
argparser.add_argument("-r", "--regex", type=str, default='.+\\n',
                       help="only apply the prefix to lines which match this regular expression")
args = argparser.parse_args()
prefix = args.prefix
regex = re.compile(args.regex)

with io.open(args.input_filename) as input_file, io.open(args.output_filename, mode='w') as output_file: 
  for line in input_file:
    if regex.search(line):
      line = prefix + line
    output_file.write(prefix + line)
