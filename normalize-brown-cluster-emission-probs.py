import argparse
import io
import gzip
from collections import defaultdict
from math import log

# parse/validate arguments
argParser = argparse.ArgumentParser()
argParser.add_argument("-brown", help="(input) output of brown clusters file")
argParser.add_argument("-prob", help="(output) log p(word|class) file")
argParser.add_argument("-encoding", default="utf8", help="input and output file encoding, defaults to utf8")
args = argParser.parse_args()

marginals = defaultdict(int)
with io.open(args.brown, encoding=args.encoding) as brown_file:
  for line in brown_file:
    (_class, word, count) = line.split('\t')
    marginals[_class] += int(count)

with io.open(args.brown, encoding=args.encoding) as brown_file, io.open(args.prob, encoding=args.encoding, mode='w') as prob_file:
  for line in brown_file:
    (_class, word, count) = line.split('\t')
    logprob = log(int(count) * 1.0 / marginals[_class])
    prob_file.write( u'{0}\t{1}\t{2}\n'.format(_class, word, logprob) )
