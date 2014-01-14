import re
import time
import io
import sys
import argparse
from collections import defaultdict

def load_word_mapping(british_vocab_filename, american_vocab_filename):
  british_to_american_map = {}
  regex_parts = []
  for british_word, american_word in zip(io.open(british_vocab_filename, encoding='utf8'),
                                         io.open(american_vocab_filename)):
    british_to_american_map[british_word] = american_word
    regex_parts.append(british_word)
  british_regex = re.compile(ur'\b(' + u'|'.join(regex_parts) + ur')\b', re.IGNORECASE)
  return british_to_american_map, british_regex

def convert_british_to_english(british_to_american_map, british_regex, british_text):
  previous_index = 0
  american_text_parts = []
  for match in british_regex.finditer(british_text):
    american_word = british_to_american_map[match.group().lower()]
    american_line.append(british_line[previous_index:match.start()])
    american_line.append(american_word)
    previous_index = match.end()
  american_text_parts.append(british_line[previous_index:])
  return ''.join(american_text_parts)

# parse/validate arguments
argParser = argparse.ArgumentParser()
argparser.add_argument("-bvocab", required=True)
argparser.add_argument("-avocab", required=True)
argParser.add_argument("-btext", required=True)
argParser.add_argument("-atext", required=True)
args = argParser.parse_args()

map, regex = load_word_mapping(args.bvocab, args.avocab)

atext_file = io.open(args.atext, encoding='utf8', mode='w')
for british_line in io.open(args.btext, encoding='utf8', mode='r'):
  atext_file.write(convert_british_to_english(british_line))

