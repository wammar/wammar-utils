import subprocess
import gzip
import re
import time
import io
import sys
import argparse
from collections import defaultdict
import scipy
from scipy.sparse import coo_matrix
from scipy.io import savemat, loadmat

# parse/validate arguments
argparser = argparse.ArgumentParser()
argparser.add_argument("-c", "--corpus", required=True, help="input corpus")
argparser.add_argument("-a", "--alignments", required= True, help="alignments probabilities")
argparser.add_argument("-m", "--matrix", required = True, help="output binary .mat file with a sparse, squared matrix X which encodes word cooccurence statistics.")
argparser.add_argument("-v", "--vocab", required=True, help="output text file which specifies each word in the vocabulary and which dimension in X's rows and columns it corresponds to. Note the vocabulary excludes infrequent words.")
argparser.add_argument("-f", "--min_frequency", type=int, default=5, help="minimum frequency for a word to be included in the vocabulary")
argparser.add_argument("-w", "--window", type=int, default=3, help="distance between two cooccuring words in a sentence")
argparser.add_argument("-e", "--embeddings", required=True, help="output embeddings file")
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
# we no longer need the lists
freqs, row_ids, column_ids = None, None, None

# save the word ids to interpret rows and columns of the matrix
with io.open(args.vocab, encoding='utf8', mode='w') as vocab:
  for i in xrange(len(id2word)):
    vocab.write(u'{} {}\n'.format(i, id2word[i]))

# read alignment probabilities
src_ids, tgt_ids, probs = [], [], []
with io.open(args.alignments, encoding='utf8', mode='r') as alignments:
  for line in alignments:
    src, tgt, prob = line.strip().split(' ')
    prob = float(prob)
    # skip tiny probabilities
    if prob < 0.001: continue
    # skip infrequent words
    if src not in word2id or tgt not in word2id: continue
    # update the lists which will be later used to initialize a sparse scipy matrix
    src_id, tgt_id = word2id[src], word2id[tgt]
    # forward direction
    src_ids.append(src_id)
    tgt_ids.append(tgt_id)
    probs.append(prob)
    # backward direction
    src_ids.append(tgt_id)
    tgt_ids.append(src_id)
    probs.append(prob)
print 'number of nonzero alignment probabilities in the {}x{} translation matrix is {}'.format(len(id2word), len(id2word), len(probs))

# create the sparse matrix that represents translations
D1 = coo_matrix((probs, (src_ids, tgt_ids)), shape=(len(id2word), len(id2word)))
# we no longer need the lists
probs, src_ids, tgt_ids = None, None, None

# save matrices in matlab format
savemat(args.matrix, dict(X=X, D1=D1, D2=D1))

optimize using matlab. this function writes the output to files: DXDsvd40lam1.mat and timing.mat
subprocess.call(['matlab -nosplash -nodisplay -r "DXDsvd()"'], shell=True)

# now read the matrix Us from the output file DXDsvd40lam1.mat
outputs = loadmat('DXDsvd40lam1.mat')
Us = outputs['Us']
print 'Us.shape =', Us.shape

# read the vocabulary
id2word = []
with io.open(args.vocab, encoding='utf8') as vocab:
  for line in vocab:
    word_id, word = line.strip().split(' ')
    assert int(word_id) == len(id2word)
    id2word.append(word)
print 'read {} words'.format(len(id2word))

# write the embeddings file
print 'embedding of id2word[0]=', id2word[0], 'is Us[0,:] =', Us[0,:].tolist()
with io.open(args.embeddings, encoding='utf8', mode='w') as embeddings_file:
  for i in xrange(len(id2word)):
    embedding = Us[i,:].tolist()
    embeddings_file.write(id2word[i])
    for j in xrange(len(embedding)):
      embeddings_file.write(u' {}'.format(embedding[j]))
    embeddings_file.write(u'\n')
