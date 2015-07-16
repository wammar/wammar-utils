import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-o", "--output_filename")
args = argparser.parse_args()

languages = [u'cs', u'de', u'en', u'es', u'fi', u'fr', u'ga', u'hu', u'it', u'sv']
punctuation_marks = [u'.', u'%', u']', u'[', u')', u'(', u'?', u'!', u'/', u'\\', u'-', u'\'', u'"', u',']

with io.open(args.output_filename, mode='w', encoding='utf8') as output_file:
  for mark in punctuation_marks:
    cluster = u'cs:' + mark
    for language in languages[1:]:
      cluster += u'_|_' + language + u':' + mark
    for language in languages:
      output_file.write(language + u':' + mark + u' ||| ' + cluster + u'\n')
