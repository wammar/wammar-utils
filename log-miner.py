import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-i", "--input_filename")
args = argparser.parse_args()

best_update, best_uas, best_epoch = -1, -1, -1
for line in open(args.input_filename, mode='r'):
  line_splits = line.strip().split()
  if len(line_splits) > 9 and line_splits[0] == "**dev":
    current_update, current_uas, current_epoch = int(line_splits[1][6:]), float(line_splits[9]), float(line_splits[2][6:-1])
    if current_uas > best_uas:
      best_update, best_uas, best_epoch = current_update, current_uas, current_epoch

print 'best_update = {}\nbest_epoch = {}\nbest_uas = {}'.format(best_update, best_epoch, best_uas)
