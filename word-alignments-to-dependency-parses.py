import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-w", "--word_alignments_filename")
argparser.add_argument("-ci", "--conll_input_filename")
argparser.add_argument("-co", "--conll_output_filename")
args = argparser.parse_args()

with io.open(args.word_alignments_filename, encoding='utf8') as word_alignments_file, io.open(args.conll_input_filename, encoding='utf8') as conll_input_file, io.open(args.conll_output_filename, encoding='utf8', mode='w') as conll_output_file:

  sent_id = 0
  for word_alignments_line in word_alignments_file:

    # read the word alignments of the current sentence
    # zero based indexes of child -> parent
    parent = { int(mapping.split('-')[1]): int(mapping.split('-')[0]) \
                   for mapping in word_alignments_line.strip().split() }
  
    # read and write conll lines of the current sentence
    conll_lines_counter = 0
    while(True):
      conll_fields = conll_input_file.readline().strip().split('\t')
      if len(conll_fields) <= 1: 
        conll_output_file.write(u'\n')
        break
      conll_lines_counter += 1
      if (int(conll_fields[0]) - 1) in parent:
        conll_fields[-4] = str( 1 + parent[int(conll_fields[0]) - 1] )
      else:
        # every word that's not aligned is assumed to be root
        conll_fields[-4] = u"0"
      conll_fields[-3:] = u'-', u'-', u'-'
      conll_output_file.write(u'{}\n'.format( '\t'.join(conll_fields) ) )
    
    if conll_lines_counter < len(parent):
      print "WARNING: the conll file is shorter than the alignments file."
      break

    sent_id += 1

print sent_id, " sentences processed read/written to the conll files."

