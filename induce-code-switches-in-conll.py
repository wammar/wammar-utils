import io
import argparse
from collections import defaultdict 

argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_conll_filename", required=True)
argparser.add_argument("-o", "--output_conll_filename", required=True)
argparser.add_argument("-d", "--dictionary_filename", required=True)
argparser.add_argument("-c", "--code_switched_filename")
argparser.add_argument("-f", "--frequency", type=float, default=1.0)
argparser.add_argument("-l1", default='en')
argparser.add_argument("-l2", default='es')
args = argparser.parse_args()

# load dictionary
dictionary = defaultdict(list)
dictionary_size = 0
with io.open(args.dictionary_filename, encoding='utf8') as dictionary_file:
  for line in dictionary_file:
    l1_word, l2_word = line.strip().split(' ||| ')
    dictionary[l1_word].append(l2_word)
    dictionary_size += 1
print '# of dictionary entries:', dictionary_size
print '# of l1 words in the dictionary:', len(dictionary)
print

# map each word in l1 to words which follow it in l2 according to the code switched text
l1_word_to_l2_next_words = defaultdict(set)
l1_to_l2_transitions = 0
if args.code_switched_filename:
  for line in io.open(args.code_switched_filename, encoding='utf8'):
    tokens = line.strip().split(' ')
    for i in xrange(len(tokens)-1):
      if tokens[i].startswith(args.l1) and tokens[i+1].startswith(args.l2):
        l1_word_to_l2_next_words[ tokens[i] ].add( tokens[i+1] )
        l1_to_l2_transitions += 1
print '# of transitions from l1 to l2:', l1_to_l2_transitions
print '# of unique l1 words which has transitions:', len(l1_word_to_l2_next_words)
print

# substitute each word in l1 with its translation in l2 if this results in a bigram which has been seen in the code switched text
# if no code switched text is available, replace words with translations at the specified frequency
tokens_count, replaced_count = 1.0, 0.0
with io.open(args.input_conll_filename) as input_conll_file:
  with io.open(args.output_conll_filename, mode='w') as output_conll_file: 
    previous_word = ''
    for line in input_conll_file:
      if len(line.strip()) == 0:
        output_conll_file.write(u'\n')
        previous_word = ''
      else:
        conll_fields = line.strip().split('\t')
        token = conll_fields[1]
        if token in dictionary and (not args.code_switched_filename or previous_word != '' and previous_word in l1_word_to_l2_next_words):
          'previous token = ', previous_word
          'current token = ', token
          for l2_translation in dictionary[token]:
            if l2_translation in l1_word_to_l2_next_words[previous_word]:
              if replaced_count / tokens_count < args.frequency:
                conll_fields[1] = l2_translation
                replaced_count += 1
                break
        tokens_count += 1
        output_conll_file.write(u'\t'.join(conll_fields) + u'\n')
        previous_word = token
print '# of replacements: {} out of {} tokens. code switching rate = {}'.format(replaced_count, tokens_count, replaced_count / tokens_count)
