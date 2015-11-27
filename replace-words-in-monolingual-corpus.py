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
#example invocation:   python $wammar_utils/replace-words-in-monolingual-corpus.py -d $word_clusters -l "de:" "en:" "es:" "fr:" "id:" "it:" "ja:" "ko:" "pt:" "sv:" -i $corpus_de $corpus_en $corpus_es $corpus_fr $corpus_id $corpus_it $corpus_ja $corpus_ko $corpus_pt $corpus_sv -o corpus.langprefix -od $augmented_word_clusters
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--input-dictionary-filename", help=" Input dictionary that maps from words to word clusters. Each line specifies a unique word and what it should map to; e.g., 'en:dog ||| clusterid13458'")
argparser.add_argument("-od", "--output-dictionary-filename", help=" Output dictionary that maps from words to trivial (singleton) word clusters. Each line specifies a unique word and what it should map to; e.g., 'en:newdog ||| clusterid134513'")
argparser.add_argument("-l", "--language-prefixes", nargs="+", action="append", help=" List of strings to prefix each word in the corresponding monolingual corpus. ")
argparser.add_argument("-i", "--input-filenames", nargs="+", action="append", help=" List of input monolingual corpora. Must be of the same length as the list of language prefixes")
argparser.add_argument("-o", "--output-filename", help=" Aggregate text in the input monolingual files, but each word in the dictionary file is replaced by its corresponding clusterid and prefixed with language id. ")
args = argparser.parse_args()

# read dictionary
max_cluster_id = -1
with io.open(args.input_dictionary_filename, encoding='utf8', mode='r') as dictionary_file:
  dictionary_items = {}
  for line in dictionary_file:
    splits = line.split(' ||| ')
    assert len(splits) == 2
    if splits[0].strip() in dictionary_items:
      print u"WARNING: a word appears twice at the left side of the dictionary. I'll use the older mapping and discard the new one."
      #Old mapping is {}. New mapping is {}. I will ignore the new mapping and keep the old one.".format(splits[0].strip(), dictionary_items[splits[0].strip()], splits[1].strip())
      continue
    dictionary_items[splits[0].strip()] = splits[1].strip()
    assert(splits[1][0:9] == "clusterid")
    cluster_id = int(splits[1].strip()[9:])
    if cluster_id > max_cluster_id: max_cluster_id = cluster_id
  print 'read {} dictionary items.'.format(len(dictionary_items))

language_corpus_tuples = []
for language_prefix, corpus_filename in zip(args.language_prefixes[0],args.input_filenames[0]):
  language_corpus_tuples.append( (language_prefix, io.open(corpus_filename, encoding='utf8', mode='r'),) )

output_file = io.open(args.output_filename, encoding='utf8', mode='w')
for (language_prefix, input_file) in language_corpus_tuples:
  lines_counter, tokens_counter, replaces_counter = 0, 0, 0
  for line in input_file:
    lines_counter += 1
    splits = line.strip().split()
    for i in xrange(len(splits)):
      tokens_counter += 1
      splits[i] = language_prefix + splits[i]
      if splits[i] in dictionary_items:
        replaces_counter += 1
        splits[i] = dictionary_items[splits[i]]
      else:
        max_cluster_id += 1
        cluster_id_string = u'clusterid{}'.format(max_cluster_id)
        dictionary_items[splits[i]] = cluster_id_string
        splits[i] = cluster_id_string
    output_file.write(u'{}\n'.format(' '.join(splits)))
  print language_prefix, '{} lines read.\n{}% ({} out of {}) tokens replaced.'.format(lines_counter, 100.0 * replaces_counter / tokens_counter, replaces_counter, tokens_counter)
output_file.close()

# write dictionary
with io.open(args.output_dictionary_filename, encoding='utf8', mode='w') as dictionary_file:
  for word in dictionary_items.keys():
    dictionary_file.write(u'{} ||| {}\n'.format(word, dictionary_items[word]))
