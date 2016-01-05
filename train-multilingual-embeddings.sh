export wammar_utils="/usr1/home/wammar/wammar-utils/"
export word2vec="/usr1/home/wammar/incremental-word2vec/"
export out="/usr1/home/wammar/cluster-embeddings/"
export embeddings="$out/all_languages.clusters.m_10000+iter_10+window_3+min_count_5+size_40"

# space-delimited list of dictionaries. 
# the file extension (xx-yy) indicates the language pair is xx-yy. 
# each line in the xx-yy dictionary is formatted as "word_in_xx ||| word_in_yy".
# the words in the dicationary files should NOT be prefixed (e.g., use "dog" NOT "en:dog") 
export bilingual_dictionaries="/usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.bg-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.cs-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.da-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.de-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.el-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.es-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.fi-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.fr-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.hu-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.it-en /usr1/home/wammar/bilingual-dictionaries/word-aligned/parallel.fwdxbwd-dict.filter_at_0p1/parallel.fwdxbwd-dict.sv-en"

# space-delimited list of monolingual tokenized and lowercased corpora.
export monolingual_corpora="/usr1/home/wammar/monolingual/combo.bg /usr1/home/wammar/monolingual/combo.cs /usr1/home/wammar/monolingual/combo.da /usr1/home/wammar/monolingual/combo.de /usr1/home/wammar/monolingual/combo.el /usr1/home/wammar/monolingual/combo.en /usr1/home/wammar/monolingual/combo.es /usr1/home/wammar/monolingual/combo.fi /usr1/home/wammar/monolingual/combo.fr /usr1/home/wammar/monolingual/combo.hu /usr1/home/wammar/monolingual/combo.it /usr1/home/wammar/monolingual/combo.sv"

# space-delimited list of language prefixes. This list must be in the same order as the list of monolingual corpora.
export language_prefixes="bg: cs: da: de: el: en: es: fi: fr: hu: it: sv:"

# create output directory (and make sure it's empty, commented out to avoid an accidental disasters).
mkdir $out
#rm -rf $out/*

# create superwords.
python $wammar_utils/map-words-to-transitive-closures.py -i $bilingual_dictionaries -o $out/word_clusters -m 1000

# replace words with superwords in individual monolingual corpora. 
python $wammar_utils/replace-words-in-monolingual-corpus.py -c $out/word_clusters -l $language_prefixes -i $monolingual_corpora -o $out/corpus.langprefix

# estimate superword embeddings.
$word2vec/word2vec -train $out/corpus.langprefix -min-count 5 -window 3 -iter 10 -size 40 -type 1 -output $out/cluster_embeddings -threads 16

# repeat the same embedding for all words in a superword.
python $wammar_utils/convert-closure-embeddings-to-word-embeddings.py -i $out/cluster_embeddings -w $out/word_clusters -o $embeddings
