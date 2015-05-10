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
argparser.add_argument("-i", "--dictionary-filenames", nargs='+', action='append', help=
                       " One or more bilingual dictionaries. For example, an english-french    " +
                       " dictionary may have one line that reads 'dog ||| chien' and the       " +
                       " filename should end with '.en-fr'")
argparser.add_argument("-o", "--output-filename", help=
                       " A map from each word in each language to all words which translate" + 
                       " into it according to the dictionaries, possibly bridging multiple " +
                       " dictionaries. Each word in the output file is prefixed with the   " +
                       " language identifier used as a suffix in the dictionary filename(s)" + 
                       " Example output line: 'en:dog ||| fr:chien\tes:perro")
argparser.add_argument("-m", "--max-cluster-size", type=int, default=10, help=
                       " Ignore translation pairs which result in a cluster with size > m")
argparser.add_argument("-s", "--cluster-separator", default="_|_", help=
                       " Use this string to separate between words which belong to the same" +
                       " cluster in the output file.")
args = argparser.parse_args()

dictionary_files = {}
for filename in args.dictionary_filenames[0]:
  print filename
  splits = filename.split('.')[-1].split('-')
  assert len(splits) == 2
  lang1, lang2 = splits
  dictionary_files[(lang1, lang2)] = io.open(filename, encoding='utf8', mode='r')

# initialize the map from each word (e.g., 'en:dog') to the index of its cluster in the 
# array of clusters.
word_to_cluster_index = {}
clusters = []
dictionaries_counter, translations_counter, empty_clusters_counter = 0, 0, 0
# for each bilingual dictionary
for (src_lang, tgt_lang) in dictionary_files.keys():
  print 'processing dictionary {}, language pair: {}-{}'.format(dictionaries_counter, 
                                                                src_lang, tgt_lang)
  dictionaries_counter += 1
  # for each entry
  for line in dictionary_files[(src_lang, tgt_lang)]:
    if translations_counter % 5000 == 0: 
      print 'done processing {} dictionary items (in total)'.format(translations_counter)
    translations_counter += 1
    # read the word pair
    splits = line.strip().split(' ||| ')
    assert len(splits) == 2
    src_word = u'{}:{}'.format(src_lang, splits[0])
    tgt_word = u'{}:{}'.format(tgt_lang, splits[1])
    # if either word is new, create a cluster of size 1 for it.
    for word in [src_word, tgt_word]:
      if word not in word_to_cluster_index:
        cluster_index = len(clusters)
        clusters.append( set([word]) )
        word_to_cluster_index[word] = cluster_index
    # now merge two clusters if need be
    cluster_indexes = [word_to_cluster_index[src_word], word_to_cluster_index[tgt_word]]
    if cluster_indexes[0] == cluster_indexes[1]:
      # there's nothing to do here. these two words already map to the same cluster
      continue
    # the cluster with the smaller index is expanded, and the one with the larger index is abandoned
    smaller_index, larger_index = min(cluster_indexes), max(cluster_indexes)
    if (len(clusters[smaller_index]) + len(clusters[larger_index]) > args.max_cluster_size):
      continue
    clusters[smaller_index] |= clusters[larger_index]
    for word in clusters[larger_index]:
      word_to_cluster_index[word] = smaller_index
    clusters[larger_index] = None
    empty_clusters_counter += 1

print 'done! stats:'
print '{} = total number of words'.format(len(word_to_cluster_index))
print '{} = total number of translation pairs used'.format(translations_counter)
print '{} = total number of clusters'.format(len(clusters) - empty_clusters_counter)
print '{} = total number of dictionaries used'.format(translations_counter)

# map established. Now, persist.
print 'now, persisting...'
with io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for word in word_to_cluster_index.keys():
    output_file.write(u'{} ||| {}\n'.format(word, args.cluster_separator.join(clusters[word_to_cluster_index[word]])))
