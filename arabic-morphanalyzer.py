import re
import time
import io
import sys
import argparse
from collections import defaultdict, namedtuple
from subprocess import call

Analysis = namedtuple('Analysis', ['lex', 'stem', 'bw', 'surface'])

_mada_bin_path = None
_mada_config_path = None
def init(mada_bin_path, mada_config_path):
  global _mada_bin_path, _mada_config_path
  _mada_bin_path = mada_bin_path
  _mada_config_path = mada_config_path
  # this will improve the runtime performance if we analyze individual words in online (as opposed to batch) fashion
  # this is not implemented yet
  pass

# return value is an array of sentences (i.e. one line in the input data file)
# every sentence is an array of tokens
# every word is an array of analyses (namedtuple Analysis)
def analyze_utf8_file(input_path):
  global _mada_bin_path, _mada_config_path
  call(["perl", _mada_bin_path, "config=".format(_mada_config_path), "file={}".format(input_path)])
  # now, read the output file
  sents = []
  ma_path = input_path + ".bw.ma"
  current_surface = ''
  for ma_line in open(ma_path):
    # meta lines
    if ma_line.startswith(';;;'):
      # add a sentence
      sents.append([])
      continue
    elif ma_line.startswith(';;WORD'):
      # add a word
      sents[-1].append([])
      current_surface = ma_line[6:].strip()
      continue
    assert current_surface != ''
    # sents[-1][-1] is an array of analyses of the current token
    features = ma_line.split()
    current_lex, current_stem, current_bw = '', '', ''
    for feature in features:
      if feature.startswith('lex:'):
        current_lex = feature[4:]
      elif feature.startswith('stem:'):
        current_stem = feature[5:]
      elif feature.startswith('bw:'):
        current_bw = feature[3:].split('/')[0]
      else:
        pass
    sents[-1][-1].append( Analysis(lex=current_lex, stem=current_stem, bw=current_bw, surface=current_surface) )
  return sents

# returns a defaultdict with MADA's 'lex' field as they key and a set of surface forms as the value
def cluster_surface_by_lex(data_filename):
  lex2surface = defaultdict(set)
  sents = analyze_utf8_file(data_filename)
  for sent in sents:
    for token in sent:
      for analysis in token:
        if analysis.lex == '':
          continue
        lex2surface[analysis.lex].add(analysis.surface)
        print analysis.lex, ' => ', analysis.surface
  return lex2surface

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", help="A sentence-per-line file of text in UTF8 encoded Arabic script.")
argparser.add_argument("-o", help="output file. information here depends on the other arguments specified")
argparser.add_argument("--cluster_surface_forms", type=bool, default=False, help="(ACTION ARGUMENT) Find Arabic surface forms in the input file which have at least one MADA analysis with a similar 'lex' field. The same surface form may appear (and typically do) in several clusters. Output file is a one-cluster-per-line file.")
args = argparser.parse_args()

# hardcoded paths on allegro 
mada_path = "/opt/tools/MADA-3.1/MADA+TOKAN.pl"
config_filepath = "/opt/tools/MADA-3.1/config-files/utf8input-notokan-nodisambig.madaconfig"

init(mada_path, config_filepath)

if args.cluster_surface_forms:
  lex2surface = cluster_surface_by_lex(args.i)
  with open(args.o, mode='w') as output_file:
    for lex in lex2surface.keys():
      for surface in lex2surface[lex]:
        output_file.write(surface + ' ')
      output_file.write('\n')
    print 'SUCCESS! Surface form clusters can be found at ', args.o
else:
  # no action 
  print 'NO ACTION ARGUMENT WERE SPECIFIED'
  assert False

