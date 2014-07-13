import io
import argparse

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename", required=True)
argparser.add_argument("-o", "--output_filename", required=True)
args = argparser.parse_args()

with io.open(args.input_filename, encoding='utf8') as input_file, \
        io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for in_line in input_file:
    # read sentence in following format: [token1^postag1,token2^postag2] [2,0]
    token_tags, parents = in_line.strip().split(' ')
    token_tags = token_tags.strip(']').strip('[').split(',')
    parents = parents.strip(']').strip('[').split(',')
    assert len(parents) == len(token_tags)
    for i in xrange(len(token_tags)):
      token_tag = token_tags[i].split('^')
      if(len(token_tag) == 2):
        tag, token = token_tag
      else:
        print token_tag
        print in_line
        assert False
        
      # write sentence in conll format
      output_file.write(u'{}\t{}\t{}\t{}\t{}\t_\t{}\t_\t_\t_\n'.format(i+1, token, token, tag[0:2], tag, parents[i]))
    
    # separate conll sentences with a blank line
    output_file.write(u'\n')
