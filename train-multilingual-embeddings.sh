export wammar_utils="/home/wammar/wammar-utils/"
export word2vec="/home/wammar/incremental-word2vec/"
export out="/home/wammar/temp/"
export bilingual_dictionaries="/home/wammar/europarl-dictionaries/parallel.fwdxbwd-dict.it-en /home/wammar/europarl-dictionaries/parallel.fwdxbwd-dict.da-en"
export corpus_en="/home/gmulc/corpora/monolingual-total/en/combo.en"
export corpus_da="/home/gmulc/corpora/monolingual-total/da/combo.da"
export corpus_it="/home/gmulc/corpora/monolingual-total/it/combo.it"

# create output directory (and make sure it's empty, commented out to avoid an accidental disaster)
#mkdir $out
#rm -rf $out/*

# create superwords
#python $wammar_utils/map-words-to-transitive-closures.py -i $bilingual_dictionaries -o $out/word_clusters -m 100

# replace words with superwords in individual monolingual corpora 
#python $wammar_utils/replace-words-in-monolingual-corpus.py -c $out/word_clusters -l da: it: en: -i $corpus_da $corpus_it $corpus_en -o $out/corpus.langprefix

# estimate superword embeddings
#$word2vec/word2vec -train $out/corpus.langprefix -min-count 5 -window 3 -iter 1 -size 40 -type 1 -output $out/cluster_embeddings

# repeat the same embedding for all words in a superword
python $wammar_utils/convert-closure-embeddings-to-word-embeddings.py -i $out/cluster_embeddings -o $out/embeddings -w $out/word_clusters
