import re
import time
import io
import sys
import argparse
from collections import defaultdict

# given one or more bilingual dictionaries, establish a map from each word in
# each language to the set of all words which translate into it according to 
# the bilingual dictionaries

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--dictionary-filename", help=
                       " Each line specifies a unique word and what it should map to; e.g., 'en:dog ||| en:dog_|_fr:chien'")
argparser.add_argument("-i", "--input-filename", help=" Input tokenized text.")
argparser.add_argument("-o", "--output-filename", help=
                       " The same text in the input file, but each word in the dictionary file is replaced " + 
                       " by its correspondence. ")
argparser.add_argument("-l", "--language-prefix", help=
                       " The string specified here will prefix each token in the output file.")
args = argparser.parse_args()

# read dictionary
with io.open(args.dictionary_filename, encoding='utf8', mode='r') as dictionary_file:
  dictionary_items = {}
  for line in dictionary_file:
    splits = line.split(' ||| ')
    assert len(splits) == 2
    if splits[0].strip() in dictionary_items:
      print u"WARNING: '{}' appears twice at the left side of the dictionary. Old mapping is {}. New mapping is {}. I will ignore the new mapping and keep the old one.".format(splits[0].strip(), dictionary_items[splits[0].strip()], splits[1].strip())
      continue
    dictionary_items[splits[0].strip()] = splits[1].strip()
  print 'read {} dictionary items.'.format(len(dictionary_items))

with io.open(args.input_filename, encoding='utf8', mode='r') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  lines_counter, tokens_counter, replaces_counter = 0, 0, 0
  for line in input_file:
    lines_counter += 1
    splits = line.strip().split()
    for i in xrange(len(splits)):
      tokens_counter += 1
      splits[i] = args.language_prefix + splits[i]
      if splits[i] in dictionary_items:
        replaces_counter += 1
        splits[i] = dictionary_items[splits[i]]
    output_file.write(u'{}\n'.format(' '.join(splits)))

print '{} lines read.\n{}% ({} out of {}) tokens replaced.'.format(lines_counter, 100.0 * replaces_counter / tokens_counter, replaces_counter, tokens_counter)

