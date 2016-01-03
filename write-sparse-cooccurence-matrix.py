import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict
import scipy
from scipy.sparse import coo_matrix
from scipy.io import savemat

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-c", "--corpus", help="input corpus")
argparser.add_argument("-m", "--matrix", help="output binary .mat file with a sparse, squared matrix X which encodes word cooccurence statistics.")
argparser.add_argument("-v", "--vocab", help="output text file which specifies each word in the vocabulary and which dimension in X's rows and columns it corresponds to. Note the vocabulary excludes infrequent words.")
argparser.add_argument("-f", "--min_frequency", type=int, default=5, help="minimum frequency for a word to be included in the vocabulary")
argparser.add_argument("-w", "--window", type=int, default=3, help="distance between two cooccuring words in a sentence")
args = argparser.parse_args()

# compute word frequencies
tokens_counter = 0
word2freq = {}
with io.open(args.corpus, encoding='utf8') as corpus:
  for line in corpus:
    tokens = line.strip().split(' ')
    for token in tokens:
      if token not in word2freq: word2freq[token] = 0
      word2freq[token] += 1
      tokens_counter += 1
print 'corpus has', tokens_counter, 'tokens, and', len(word2freq), 'word types'

# filter out low frequency words from the vocabulary, and give each word a unique id
id2word = []
for word in word2freq.keys():
  if word2freq[word] < args.min_frequency: 
    del word2freq[word]
    continue
  word2freq[word] = len(id2word)
  id2word.append(word)
# the values of the dictionary now are word ids
word2id = word2freq
# add sentence boundary words
SOS, EOS = u'<s>', u'</s>'
if SOS not in word2id:
  word2id[SOS] = len(id2word)
  id2word.append(SOS)
if EOS not in word2id:
  word2id[EOS] = len(id2word)
  id2word.append(EOS)
SOS_ID, EOS_ID = word2id[SOS], word2id[EOS]
print 'after excluding infrequent words, vocabulary size =', len(id2word)

# compute cooccurence statistics
word_context2freq = defaultdict(float)
updates_counter = 0
window_offsets = range(-args.window, 0) + range(1, args.window+1)
with io.open(args.corpus, encoding='utf8') as corpus:
  for line in corpus:
    # read a sentence
    splits = line.strip().split(' ')
    word_ids = []
    # first, insert SOS tokens
    for i in xrange(args.window):
      word_ids.append(SOS_ID)
    # then add frequent words
    for token in splits:
      if token not in word2id: continue
      word_ids.append(word2id[token])
    # then add EOS tokens
    for i in xrange(args.window):
      word_ids.append(EOS_ID)
    filtered_sent = []
    for i in xrange(len(word_ids)):
      filtered_sent.append(id2word[word_ids[i]])
    print ' '.join(filtered_sent)
    # update word_context2freq
    for token_index in xrange(args.window, len(word_ids) - args.window):
      focus_word_id = word_ids[token_index]
      for context_offset in window_offsets:
        context_word_id = word_ids[token_index + context_offset]
        word_context2freq[(focus_word_id, context_word_id,)] += 1
        updates_counter += 1
print 'updates_counter =', updates_counter
print 'len(word_context2freq) =', len(word_context2freq)

# create three lists that summarize the data: row_ids, column_ids, freqs
row_ids, column_ids, freqs = [], [], []
for row_col, freq in word_context2freq.iteritems():
  row_id, column_id = row_col
  row_ids.append(row_id)
  column_ids.append(column_id)
  freqs.append(freq)
# we no longer need the dictionary
word_context2freq = None

# create the sparse matrix
X = coo_matrix((freqs, (row_ids, column_ids)), shape=(len(id2word), len(id2word)))
savemat(args.matrix, dict(X=X))

# save the word ids to interpret rows and columns of the matrix
with io.open(args.vocab, encoding='utf8', mode='w') as vocab:
  for i in xrange(len(id2word)):
    vocab.write(u'{} {}\n'.format(i, id2word[i]))
