import io
import argparse
from common_typos import lang2typo2correct
import random
from collections import defaultdict

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
argparser.add_argument("-f", "--frequency", type=float, required=True, 
                       help="Frequency of typos to incude (per word, between 0 and 1).")
argparser.add_argument("-l", "--language", default='en', help="2-letter code of language.")

args = argparser.parse_args()

# process lang2typo2correct
if args.language not in lang2typo2correct:
  print 'Fatal: The specified language code', args.lagnuage, 'is not supported. The supported languages are: ', ' '.join(lang2typo2correct.keys())
  exit(1)
correct2typos = defaultdict(list)
for (typo, correct) in lang2typo2correct[args.language]:
  correct2typos[correct].append(typo)
print 'we have typos for ', len(correct2typos), 'correct words.'

tokens_count, typos_count = 1.0, 0.0

with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    for line in input_file:
      if len(line.strip()) == 0:
        output_file.write(u'\n')
      else:
        conll_fields = line.strip().split('\t')
        correct_token = conll_fields[1]
        if correct_token in correct2typos and typos_count / tokens_count < args.frequency:
          typos = correct2typos[correct_token]
          conll_fields[1] = random.choice(typos)
          assert correct_token != conll_fields[1]
          typos_count += 1
        tokens_count += 1
        output_file.write(u'\t'.join(conll_fields) + u'\n')

print 'induced typos / all words =', typos_count, '/', tokens_count, ' = ', typos_count/tokens_count, ' vs. desired frequency = ', args.frequency
