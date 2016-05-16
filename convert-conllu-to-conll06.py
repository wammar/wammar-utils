import io
import argparse

# converts the modified conll format of universal dependency parses to that of conll 2006. 
# the main thing is to remove multi-word annotations, and remove comment lines.
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
args = argparser.parse_args()

def is_cyclic(child_to_parent_cache, child_key):
  current_parent = child_to_parent_cache[child_key]
  while True:
    if current_parent not in child_to_parent_cache: return False
    if current_parent == child_key: return True
    current_parent = child_to_parent_cache[current_parent]

sents_counter = 0
child_to_parent_cache = {}
with io.open(args.input_filename) as input_file:
  with io.open(args.output_filename, mode='w') as output_file: 
    current_sentence = []
    for line in input_file:
      if len(line) > 0 and line[0] == '#':
        continue
      if len(line.strip()) == 0 and len(current_sentence) == 0:
        continue
      elif len(line.strip()) == 0 and len(current_sentence) > 0:
        output_file.write(u''.join(current_sentence) + u'\n')
        current_sentence = []
        child_to_parent_cache = {}
        sents_counter += 1
      else:
        conll_fields = line.strip().split('\t')
        # Skip lines which describe multiple words since each of the individual words has a separate line.
        if '-' in conll_fields[0]: continue
        # projected treebanks sometimes use head=-1 to indicate (multiple) roots
        if int(conll_fields[6]) < 0: conll_fields[6] = "0"
        # detect (some) circular dependencies and break them by assuming the later one is rooted at 0
        child_to_parent_cache[conll_fields[0]] = conll_fields[6]
        if is_cyclic(child_to_parent_cache, conll_fields[0]): 
          print 'WARNING: sentence #', sents_counter, 'has a cycle. child_to_parent_cache is:\n', child_to_parent_cache
          conll_fields[6] = "0"
          child_to_parent_cache[conll_fields[0]] = conll_fields[6]
          print 'to resolve this, i updated child_to_parent_cache as follows:\n', child_to_parent_cache, '\n'
        # remove language specific extensions of dependency relationships.
        if ':' in conll_fields[7]: conll_fields[7] = conll_fields[7][:conll_fields[7].find(':')]
        # replace - with _ in POS fields
        conll_fields[3] = conll_fields[3].replace('-', '_')
        conll_fields[4] = conll_fields[4].replace('-', '_')
        # remove spaces from the second and third fields
        conll_fields[1] = conll_fields[1].replace(' ', '')
        conll_fields[2] = conll_fields[1].replace(' ', '')
        line = u'\t'.join(conll_fields)+u'\n'
        current_sentence.append(line)

    # consumed all lines in input file
    if len(current_sentence) > 0:
      output_file.write(u''.join(current_sentence) + u'\n')
      current_sentence = []
