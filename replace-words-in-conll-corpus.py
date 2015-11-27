import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--dictionary-filename", help=
                       " Each line specifies a unique word and what it should map to; e.g., 'en:dog ||| clusterid413'")
argparser.add_argument("-i", "--input-filename", help=" Input conllx-formatted file.")
argparser.add_argument("-o", "--output-filename", help=
                       " Output conll-formatted file where each surface form is replaced with another string according to the map. ")
argparser.add_argument("-c", "--cluster-map-filename", help=" Output file, each line consists of 3 space-delimited strings: cluster_id, language_id and surface form. ")
argparser.add_argument("-p", "--use-language-prefix", action='store_true', help=" Prefix the corresponding value in the map with the original language prefix of the key (i.e., of the surface form). ")
args = argparser.parse_args()

# read dictionary
with io.open(args.dictionary_filename, encoding='utf8', mode='r') as dictionary_file:
  dictionary_items = {}
  for line in dictionary_file:
    splits = line.split(' ||| ')
    assert len(splits) == 2
    if splits[0].strip() in dictionary_items:
      print u"WARNING: a word appears twice at the left side of the dictionary. I'll use the older mapping and discard the new one."
      #Old mapping is {}. New mapping is {}. I will ignore the new mapping and keep the old one.".format(splits[0].strip(), dictionary_items[splits[0].strip()], splits[1].strip())
      continue
    dictionary_items[splits[0].strip()] = splits[1].strip()
  print 'read {} dictionary items.'.format(len(dictionary_items))

cluster_language_to_word = {}

with io.open(args.input_filename, encoding='utf8', mode='r') as input_file, io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  lines_counter = 0
  tokens_found, tokens_not_found = 0, 0
  for line in input_file:
    lines_counter += 1
    splits = line.strip().split('\t')
    if len(line.strip()) == 0:
      output_file.write(u'\n')
      continue
    if len(splits) == 1:
      print 'FATAL: malformatted input file, especially the line: '
      print line
      assert False
    if len(splits[1]) <= 3 or splits[1][2] != ':':
      print 'FATAL: surface forms must be prefixed with the two-letter ISO code of the language followed by a colon such as "en:decision"'
      print 'the following surface form does not: ' + splits[1]
      assert False
    if splits[1] in dictionary_items:
      mapped_value = dictionary_items[splits[1]]
      tokens_found += 1
    else:
      mapped_value = 'UNK_CLUSTER'
      tokens_not_found += 1
    if args.use_language_prefix:
      # map (cluster, language) -> word 
      # note that the same cluster may have multiple words from the same language in which case the one that appears later in the treebank will be written to the output file.
      cluster_language_to_word[(mapped_value, splits[1][:2])] = splits[1][3:]
      # replace the surface string with the cluster id
      splits[1] = splits[1][:3] + mapped_value
    else:
      splits[1] = mapped_value
    output_file.write(u'{}\n'.format('\t'.join(splits)))

print '{} lines read.\n{}% ({} out of {}) token coverage.'.format(lines_counter, 100.0 * tokens_found / (tokens_found + tokens_not_found), tokens_found, tokens_found + tokens_not_found)

with io.open(args.cluster_map_filename, encoding='utf8', mode='w') as clusters_file:
  for cluster_language in cluster_language_to_word.keys():
    (cluster, language) = cluster_language
    clusters_file.write(u'{} {} {}\n'.format(cluster, language, cluster_language_to_word[cluster_language]))
