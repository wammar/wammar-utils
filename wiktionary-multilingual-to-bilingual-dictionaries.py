import io
import re
from collections import defaultdict
import argparse
import gzip
import os

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-rawfile", "--rawfile", help="The raw file at http://downloads.dbpedia.org/wiktionary/dumps/de/wiktionary_de+en_2012-04-01_translations.csv.gz, or regenerate the file yourself using instructions at http://dbpedia.org/Wiktionary.", required=True)
argparser.add_argument("-outdir", "--outdir", help='The output directory where bilingual dictionary files will be created. The filename will be "srclang-tgtlang", with each line consisting of "src_word ||| tgt_word". This is the same format specified https://github.com/mfaruqui/eacl14-cca. Note that each pair of languages will have two distinct but equivalent files (e.g., "English-Arabic" and "Arabic-English"). While this is wasteful, it allows the output files to be directly used with Manaal Faruqui\'s library at https://github.com/mfaruqui/eacl14-cca.', required=True)
argparser.add_argument("-langs", "--langs", help="Case insensitive regular expression which can only be found in the languages of interest. For example: english|arabic|french|chinese. By default, all languages are of interest.", default=".+")
argparser.add_argument("-phrases", "--phrases", help="By default, ignore phrases of more than one word at the source and/or target.", action='store_true')
argparser.add_argument("-lowercase", "--lowercase", help="Lowercase? Turned off by default", action='store_true')
args = argparser.parse_args()

def NormalizeLanguageName(raw_name, regex_full_match):
  return regex_full_match.lower()

def NormalizeWord(raw_word):
  normalized = raw_word.replace('_', ' ').replace(r"\'", "'").replace("#", "")
  if ' ' in normalized and not args.phrases: normalized = ''
  if args.lowercase: normalized = normalized.lower()
  return normalized

# languages of interest
lang_of_interest = re.compile(args.langs, flags=re.IGNORECASE)

# read translations
lang1_lang2_word1_word2 = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
lines_counter = 0
with gzip.open(args.rawfile) as rawfile:
  for in_line in rawfile:
    in_line = in_line.decode('utf8')
    lines_counter += 1
    splits = in_line[1:-2].split('","')
    src_word, src_lang, src_pos, src_desc, tgt_word, tgt_lang = splits
    src_lang_match, tgt_lang_match = lang_of_interest.search(src_lang), lang_of_interest.search(tgt_lang)
    # only process word pairs where both source and target languages are of interest 
    if not src_lang_match or not tgt_lang_match: continue
    # normalize language names (potentially conflating different languages)
    src_lang, tgt_lang = NormalizeLanguageName(src_lang, src_lang_match.group()), NormalizeLanguageName(tgt_lang, tgt_lang_match.group())
    if src_lang == tgt_lang: continue
    # normalize words
    src_word, tgt_word = NormalizeWord(src_word), NormalizeWord(tgt_word)
    if min(len(src_word), len(tgt_word)) == 0: continue
    lang1_lang2_word1_word2[src_lang][tgt_lang][src_word].add(tgt_word)
    lang1_lang2_word1_word2[tgt_lang][src_lang][tgt_word].add(src_word)

# write translations
if not os.path.exists(args.outdir): os.makedirs(args.outdir)
bad_word_pairs = 0
good_word_pairs = 0
bad_language_pairs = {}
good_language_pairs = set()

language_name_to_iso={'czech':'cs', 'german':'de', 'english':'en', 'spanish':'es',
                      'finnish':'fi', 'french':'fr', 'irish':'ga', 'hungarian':'hu',
                      'italian':'it', 'swedish':'sv', 'bulgarian':'bg', 'danish':'da',
                      'greek':'el', 'persian':'fa', 'croatian':'hr', 'hebrew':'he',
                      'basque':'eu', 'indonesian':'id', 'japanese':'ja', 'korean':'ko',
                      'portuguese':'pt', 'estonian':'et', 'lithuanian':'lt', 'latvian':'lv',
                      'dutch':'nl', 'polish':'pl', 'romanian':'ro', 'slovak':'sk', 
                      'slovene':'sl'}
for src_lang in lang1_lang2_word1_word2.keys():
  for tgt_lang in lang1_lang2_word1_word2[src_lang].keys():
    src_lang_iso = language_name_to_iso[src_lang] if src_lang in language_name_to_iso else src_lang
    tgt_lang_iso = language_name_to_iso[tgt_lang] if tgt_lang in language_name_to_iso else tgt_lang
    try: 
      print 'writing to {}/wiktionary.{}-{}'.format(args.outdir, src_lang_iso, tgt_lang_iso)
    except:
      bad_language_pairs[src_lang+'<=>'+tgt_lang] = lang1_lang2_word1_word2[src_lang][tgt_lang]
      continue
    good_language_pairs.add(src_lang+u'<=>'+tgt_lang)
    with open('{}/wiktionary.{}-{}'.format(args.outdir, src_lang_iso, tgt_lang_iso), mode='w') as outfile:
      for (src_word, tgt_words_set) in lang1_lang2_word1_word2[src_lang][tgt_lang].iteritems():
        for tgt_word in tgt_words_set:
          try: 
            outfile.write(u'{} ||| {}\n'.format(src_word, tgt_word).encode('utf8'))
          except:
            bad_word_pairs += 1
            continue
          good_word_pairs += 1
    
print good_word_pairs, 'word pairs were written in', len(good_language_pairs), ' unique language pairs (one file per language pair).'
print bad_word_pairs, 'word pairs were not written to files (encoding issues).'
print len(bad_language_pairs), 'language pairs were not written to files (filenames must be ASCII-encoded).'
