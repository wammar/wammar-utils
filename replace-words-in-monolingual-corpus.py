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
argparser.add_argument("-c", "--clusters-filename", help=" Each line specifies the cluster of one word, and is formatted as three tab-delimited strings: cluster_id, word, and an obsolete frequency value; e.g., 'clusterid13458   en:dog  10'. The cluster information are first read from this file, then extended to include new words in the monolingual corpus, then written back to the same file.")
argparser.add_argument("-l", "--language-prefixes", nargs="+", action="append", help=" List of strings to prefix each word in the corresponding monolingual corpus. ")
argparser.add_argument("-i", "--input-filenames", nargs="+", action="append", help=" List of input monolingual corpora. Must be of the same length as the list of language prefixes")
argparser.add_argument("-o", "--output-filename", help=" Aggregate text in the input monolingual files, but each word in the clusters file is replaced by its corresponding clusterid and prefixed with language id. ")
args = argparser.parse_args()

# read clusters
max_cluster_id = -1
with io.open(args.clusters_filename, encoding='utf8', mode='r') as clusters_file:
  word2cluster = {}
  for line in clusters_file:
    splits = line.split('\t')
    assert len(splits) == 3
    cluster, word, dummy = splits
    if word in word2cluster:
      print u"WARNING: a word appears twice in the clusters file. I'll use the older mapping and discard the new one."
      continue
    word2cluster[word] = cluster
    assert(cluster[0:9] == "clusterid")
    cluster_id = int(cluster[9:])
    if cluster_id > max_cluster_id: max_cluster_id = cluster_id
  print 'read {} words from the clusters file.'.format(len(word2cluster))

language_corpus_tuples = []
for language_prefix, corpus_filename in zip(args.language_prefixes[0],args.input_filenames[0]):
  language_corpus_tuples.append( (language_prefix, io.open(corpus_filename, encoding='utf8', mode='r'),) )

output_file = io.open(args.output_filename, encoding='utf8', mode='w')
for (language_prefix, input_file) in language_corpus_tuples:
  lines_counter, tokens_counter = 0, 0
  for line in input_file:
    lines_counter += 1
    splits = line.strip().split(' ')
    for i in xrange(len(splits)):
      tokens_counter += 1
      splits[i] = language_prefix + splits[i]
      if splits[i] in word2cluster:
        splits[i] = word2cluster[splits[i]]
      else:
        max_cluster_id += 1
        cluster_id_string = u'clusterid{}'.format(max_cluster_id)
        word2cluster[splits[i]] = cluster_id_string
        splits[i] = cluster_id_string
    output_file.write(u'{}\n'.format(' '.join(splits)))
  print language_prefix, '{} lines read. {} tokens replaced.'.format(lines_counter, tokens_counter)
output_file.close()

# write dictionary
with io.open(args.clusters_filename, encoding='utf8', mode='w') as dictionary_file:
  for word in word2cluster.keys():
    dictionary_file.write(u'{}\t{}\t10\n'.format(word2cluster[word], word))

print 'wrote {} words to the clusters file.'.format(len(word2cluster))
