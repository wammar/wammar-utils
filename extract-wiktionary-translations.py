import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict
from iso_639_1_codes import iso_639_1_name2code, iso_639_1_code2name

def extract_dictionary(xml_dump_filename, languages, allow_phrases):
  translations = []
  current_word = None
  current_language = None
  is_reading_translations = False
  counter = 0
  for line in io.open(xml_dump_filename, encoding='utf8'):
    # let the user know what's going on.
    if counter % 100000 == 0: sys.stdout.write('\r{} lines read'.format(counter))
    counter += 1

    line = line.strip()

    # process new word
    if line.startswith('<title>'):
      current_word = line[7:-8]

    # process current language
    elif line.endswith('==') and len(line) > 3 and line[-3] != '=':
      language_name = line[line.find('==')+2:-2]
      if language_name not in iso_639_1_name2code: iso_639_1_name2code[language_name] = ''
      current_language = iso_639_1_name2code[language_name]

    # start reading translations
    elif line == '=====Translations=====':
      is_reading_translations = True
    
    # read a translation (potentially)
    elif is_reading_translations and line.startswith('* '):
      # read the target language
      colon_index = line.find(':')
      if colon_index == -1: continue
      other_language_name = line[2:colon_index]
      if other_language_name not in iso_639_1_name2code: iso_639_1_name2code[other_language_name] = ''
      other_language = iso_639_1_name2code[other_language_name]
      if not current_language or not other_language: continue

      # read the translations
      for translation in line[colon_index+1:].split(','):
        translation = translation.strip()
        #print current_word, '->', translation
        if translation[:2] != '{{' or translation[-2:] != '}}': continue
        splits = translation[2:-2].split('|')
        #print current_word, '->', splits
        if len(splits) < 3 or splits[1] != other_language: continue
        translated_word = splits[2]
        #print current_word, '->', translated_word
        # skip phrases if not allowed
        if (not allow_phrases) and (current_word.find(' ') > -1 or translated_word.find(' ') > -1): continue
        pair = (u'{}:{}'.format(current_language, current_word), u'{}:{}'.format(other_language, translated_word),)
        #print pair
        translations.append(pair)
      
    # stop reading translations
    elif is_reading_translations and line.startswith('='):
      is_reading_translations = False

  # processed all lines in the xml file
  return translations

def main(argv):
  # parse/validate arguments
  argparser = argparse.ArgumentParser()
  argparser.add_argument("-i", "--input_dump", help='English wiktionary articles dump file, uncompressed')
  argparser.add_argument("-o", "--output_dictionary", help='A multilingual dictionary of word pairs')
  argparser.add_argument("-p", "--allow_phrases", action='store_true', help="Allow phrases")
  argparser.add_argument("-l", "--languages", help='Comma-separated list of ISO 639-1 codes of languages of interest')
  args = argparser.parse_args()
  multilingual_dictionary = extract_dictionary(args.input_dump, args.languages.split(','), args.allow_phrases)
  language2count = defaultdict(int)
  with io.open(args.output_dictionary, encoding='utf8', mode='w') as multilingual_dictionary_file:
    for (word1, word2) in multilingual_dictionary:
      language2count[word1[:2]] += 1
      language2count[word2[:2]] += 1
      multilingual_dictionary_file.write(u'{} ||| {}\n'.format(word1, word2))
  for language, count in language2count.iteritems():
    print language, count

if __name__ == '__main__':
  main(sys.argv)

