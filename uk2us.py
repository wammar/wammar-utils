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
    british_word, american_word = british_word.strip(), american_word.strip()
    british_to_american_map[british_word] = american_word
    regex_parts.append(british_word)
  british_regex = re.compile(ur'\b(' + u'|'.join(regex_parts) + ur')\b', re.IGNORECASE)
  return british_to_american_map, british_regex

def convert_british_to_english(british_to_american_map, british_regex, british_text):
  previous_index = 0
  american_text_parts = []
  for match in british_regex.finditer(british_text):
    american_word = british_to_american_map[match.group().lower()]
    american_text_parts.append(british_line[previous_index:match.start()])
    american_text_parts.append(american_word)
    previous_index = match.end()
  american_text_parts.append(british_line[previous_index:])
  return ''.join(american_text_parts)

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-bvocab", default="british_english.txt", help="Source side of a British-American bilingual dictionary")
argparser.add_argument("-avocab", default="american_english.txt", help="Target side of a British-American bilingual dictionary")
argparser.add_argument("-btext", required=True, help="Input filename of British English text")
argparser.add_argument("-atext", required=True, help="Output filename of American English text")
args = argparser.parse_args()

british_to_american_map, british_regex = load_word_mapping(args.bvocab, args.avocab)

atext_file = io.open(args.atext, encoding='utf8', mode='w')
for british_line in io.open(args.btext, encoding='utf8', mode='r'):
  atext_file.write(convert_british_to_english(british_to_american_map, british_regex, british_line))

