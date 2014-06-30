 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import argparse
import re, sys, io

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-i", "--input_filename", required=True, help="normal arabic in utf8")
arg_parser.add_argument("-o", "--output_filename", required=True, help="normalized arabic")
args = arg_parser.parse_args()

kashida_re = re.compile(u'[ـ]')
haa_re =  re.compile(u'[هة]')
yaa_re =  re.compile(u'[يى]')
alef_re =  re.compile(u'[أإآ]')
# http://symbolcodes.tlt.psu.edu/bylanguage/arabicchart.html#vowel
vowels_re = re.compile(u'[\u1611]')
with io.open(args.output_filename, encoding='utf8', mode='w') as output_file:
  for line in io.open(args.input_filename, encoding='utf8'):
    line, _ = re.subn(alef_re, u'ا', line)
    line, _ = re.subn(kashida_re, u'', line)
    line, _ = re.subn(haa_re, u'ه', line)
    line, _ = re.subn(yaa_re, u'ي', line)
    line, _ = re.subn(vowels_re, u'', line)
    output_file.write( line )

