import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict
import csv

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-sswl", help="csv file downloaded from kimono labs' api for crawling sswl, e.g., sswl_features.csv in this repository")
argparser.add_argument("-wals", help="csv file downloaded from wals, e.g., wals_features.csv in this repository")
argparser.add_argument("-pat", help="modified typological features provided by Patrick Littell <puchitao@gmail.com>")
argparser.add_argument("-ov", "--output_vectors", help="one language per row. features are binary encoded.")
argparser.add_argument("-zhang15", action="store_true", help="only use the WALS features Zhang and Barzilay 2010 used, namely: 82a,83a,85a,86a,87a")
argparser.add_argument("-genus", action="store_true", help="only use the genus feature in WALS")
args = argparser.parse_args()

genus_feature_id = 'wals_genus'

zhang15_feature_ids = set(['wals_82a_order_of_subject_and_verb', # used by zhang15 but not naseem10
                            'wals_83a_order_of_object_and_verb', # used by zhang15 but not naseem10
                            #'wals_81a_order_of_subject,_object_and_verb', # used by naseem10 but not zhang15
                            #'wals_81b_languages_with_two_dominant_orders_of_subject,_object,_and_verb',
                            'wals_85a_order_of_adposition_and_noun_phrase',
                            'wals_86a_order_of_genitive_and_noun',
                            'wals_87a_order_of_adjective_and_noun'])
                            #'wals_88a_order_of_demonstrative_and_noun', # used by naseem10 but not zhang15
                            #'wals_89a_order_of_numeral_and_noun' # used by naseem10 but not zhang15

lang_to_feature_id_to_value = defaultdict(lambda: defaultdict(str))
lang_code_to_name = { 'bg' : 'bulgarian',
                      'cs' : 'czech',
                      'da' : 'danish',
                      'de' : 'german',
                      #'el' : 'greek',
                      'en' : 'english',
                      'es' : 'spanish',
                      'eu' : 'basque',
                      #'fa' : 'persian',
                      'fi' : 'finnish',
                      'fr' : 'french',
                      'ga' : 'irish',
                      'he' : 'hebrew',
                      'hu' : 'hungarian',
                      #'hr' : 'croatian',
                      'id' : 'indonesian',
                      'it' : 'italian',
                      'ja' : 'japanese',
                      'ko' : 'korean',
                      'pt' : 'portuguese',
                      'sv' : 'swedish' }

lang_name_to_code = { v: k for k, v in lang_code_to_name.items() }
lang_name_to_code['hebrew (modern)'] = lang_name_to_code['hebrew']
global_feature_id_to_values = defaultdict(set)

# read sswl features
with open(args.sswl, mode='rb') as sswl_file:
  sswl_reader = csv.reader(sswl_file, delimiter=',', quotechar='"')
  # each row describes one feature for one language
  for row_fields in sswl_reader:
    # skip header file
    if len(row_fields) > 0 and row_fields[0] == 'sswl_property_id.href': continue 

    # we're not interested in collection 2 extracted by kimonolabs
    if len(row_fields) > 0 and row_fields[0] == 'property3': break

    # each relevant row consists of five fields
    assert(len(row_fields) == 5)
    (feature_url, feature_name, feature_value, row_id, lang_url) = row_fields
    lang_name = lang_url.split('/')[-1].lower()

    # skip languages we don't care about
    if lang_name not in lang_name_to_code: continue

    # save this value
    lang_code = lang_name_to_code[lang_name]
    feature_id = 'sswl_' + feature_name.replace(' ', '_').lower()
    feature_value = feature_value.replace(' ', '_').lower()
    lang_to_feature_id_to_value[lang_code][feature_id] = feature_value
    global_feature_id_to_values[feature_id].add(feature_value)

# read wals features
with open(args.wals, mode='rb') as wals_file:
  wals_reader = csv.reader(wals_file, delimiter=',', quotechar='"')
  wals_feature_ids = None

  # each row describes one language
  for row_fields in wals_reader:
    
    # read the header
    if not wals_feature_ids:
      assert(row_fields[3] == 'Name')
      wals_feature_ids = []
      for field in row_fields:
        wals_feature_ids.append('wals_' + field.replace(' ', '_').lower())
      # done with the header
      continue

    # identify the language
    lang_name = row_fields[3].lower()
    if lang_name not in lang_name_to_code: continue
    lang_code = lang_name_to_code[lang_name]

    # read all features of this language
    for field_index in range(6, len(wals_feature_ids)):
      feature_id = wals_feature_ids[field_index]
      feature_value = row_fields[field_index].replace(' ', '_').lower()
      lang_to_feature_id_to_value[lang_code][feature_id] = feature_value
      global_feature_id_to_values[feature_id].add(feature_value)

# now, only keep features which are specified for all languages of interest.
# count number of languages specified for each language
feature_id_to_count_of_specified_languages = defaultdict(int)
for lang_code in lang_to_feature_id_to_value.keys():
  for feature_id in lang_to_feature_id_to_value[lang_code].keys():
    if lang_to_feature_id_to_value[lang_code][feature_id] == '': continue
    feature_id_to_count_of_specified_languages[feature_id] += 1

# remove unwanted features
for lang_code in lang_to_feature_id_to_value.keys():
  for feature_id in list(lang_to_feature_id_to_value[lang_code].keys()):
    # if we're only doing zhang15 features, delete everything else.
    if args.zhang15:
      if feature_id not in zhang15_feature_ids: 
        del lang_to_feature_id_to_value[lang_code][feature_id]
        if feature_id in global_feature_id_to_values: del global_feature_id_to_values[feature_id]
    # if we're only doing genus features, delete everything else.
    elif args.genus:
      if feature_id != genus_feature_id:
        del lang_to_feature_id_to_value[lang_code][feature_id]
        if feature_id in global_feature_id_to_values: del global_feature_id_to_values[feature_id]
    # otherwise, delete features that are not specified for all languages
    else:
      if feature_id_to_count_of_specified_languages[feature_id] != len(lang_to_feature_id_to_value):
        del lang_to_feature_id_to_value[lang_code][feature_id]
        if feature_id in global_feature_id_to_values: del global_feature_id_to_values[feature_id]

# debug
for feature_id in global_feature_id_to_values:
  print feature_id, 'is only specified for', feature_id_to_count_of_specified_languages[feature_id], 'out of', len(lang_to_feature_id_to_value), 'languages'

# print the remaining values
print len(lang_to_feature_id_to_value)
for lang_code in lang_to_feature_id_to_value.keys():
  print '=='
  print lang_code
  print '=='
  for feature_id, feature_value in sorted(lang_to_feature_id_to_value[lang_code].items()):
    print lang_code, feature_id
    print '\t' + feature_value

print '\n\nalmost done\n\n'
with open(args.output_vectors, mode='w') as output_vectors_file:
  # first line is a header
  output_vectors_file.write('#')
  fields = ['lang_code']
  for feature_id in sorted(global_feature_id_to_values.keys()):
    for feature_value in global_feature_id_to_values[feature_id]:
      fields.append('{}={}'.format(feature_id, feature_value))
  output_vectors_file.write(' '.join(fields) + '\n')
  
  # write one language per line
  for lang_code in sorted(lang_to_feature_id_to_value.keys()):
    fields = [lang_code]
    # for each feature_id=feature_value, write a binary value
    for feature_id in sorted(global_feature_id_to_values.keys()):
      for feature_value in global_feature_id_to_values[feature_id]:
        fields.append('1' if lang_to_feature_id_to_value[lang_code][feature_id] == feature_value else '0')
    output_vectors_file.write(' '.join(fields) + '\n')
