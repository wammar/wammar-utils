import io
import argparse
import re

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-p", "--prefix", type=str, required=True, 
                       help="the string to prefix lines.")
argparser.add_argument("-r", "--regex", type=str, default='.+\\n',
                       help="only apply the prefix to lines which match this regular expression")
argparser.add_argument("-remove-prefix", action='store_true', help='Instead of inserting the prefix, remove it (when it exists)')
args = argparser.parse_args()
prefix = args.prefix
regex = re.compile(args.regex)

with open(args.input_filename) as input_file, open(args.output_filename, mode='w') as output_file: 
  for line in input_file:
    if regex.search(line):
      if args.remove_prefix:
        line = line[len(prefix):] if line.startswith(prefix) else line
      else:
        line = prefix + line
    output_file.write(line)
