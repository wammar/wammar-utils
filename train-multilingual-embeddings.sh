export wammar_utils="/path/to/wammar-utils/"
export word2vec="/path/to/word2vec/"
export in="/path/to/input/directory/"
export out="/path/to/output/directory/"
export corpus_cs="/path/to/monolingual/corpus"
export corpus_de="/path/to/monolingual/corpus"
export corpus_en="/path/to/monolingual/corpus"
export corpus_es="/path/to/monolingual/corpus"
export corpus_fi="/path/to/monolingual/corpus"
export corpus_fr="/path/to/monolingual/corpus"
export corpus_ga="/path/to/monolingual/corpus"
export corpus_hu="/path/to/monolingual/corpus"
export corpus_it="/path/to/monolingual/corpus"
export corpus_sv="/path/to/monolingual/corpus"

# create output directory (and make sure it's empty, commented out to avoid an accidental disaster)
mkdir $out
#rm -rf $out/*

# for each language pair, create a bilingual dictionary from fast_align's forward and backward alignments
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.cs-en -ir $in/params.en-cs -d $out/dict.cs-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.de-en -ir $in/params.en-de -d $out/dict.de-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.es-en -ir $in/params.en-es -d $out/dict.es-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.fi-en -ir $in/params.en-fi -d $out/dict.fi-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.fr-en -ir $in/params.en-fr -d $out/dict.fr-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.ga-en -ir $in/params.en-ga -d $out/dict.ga-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.hu-en -ir $in/params.en-hu -d $out/dict.hu-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.it-en -ir $in/params.en-it -d $out/dict.it-en
python $wammar_utils/filter-word-alignment-parameters.py -t 0.05 -if $in/params.sv-en -ir $in/params.en-sv -d $out/dict.sv-en

# create superwords
python $wammar_utils/map-words-to-transitive-closures.py -i $out/dict.* -o $out/word_clusters

# replace words with superwords in individual monolingual corpora 
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "cs:" -i $corpus_cs -o $out/corpus_cs.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "de:" -i $corpus_de -o $out/corpus_de.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "en:" -i $corpus_en -o $out/corpus_en.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "es:" -i $corpus_es -o $out/corpus_es.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "fi:" -i $corpus_fi -o $out/corpus_fi.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "fr:" -i $corpus_fr -o $out/corpus_fr.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "ga:" -i $corpus_ga -o $out/corpus_ga.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "hu:" -i $corpus_hu -o $out/corpus_hu.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "it:" -i $corpus_it -o $out/corpus_it.langprefix
python $wammar_utils/replace-words-in-monolingual-corpus.py -d $out/word_clusters -l "sv:" -i $corpus_sv -o $out/corpus_sv.langprefix

# aggregate monolingual corpora
cat $out/corpus_cs.langprefix $out/corpus_de.langprefix $out/corpus_en.langprefix $out/corpus_es.langprefix $out/corpus_fi.langprefix $out/corpus_fr.langprefix $out/corpus_ga.langprefix $out/corpus_hu.langprefix $out/corpus_it.langprefix $out/corpus_sv.langprefix > $out/corpus.langprefix

# estimate superword embeddings
$word2vec/word2vec -train $out/corpus.langprefix -min-frequency 40 -type 3 -threads 32 -output $out/cluster_embeddings

# repeat the same embedding for all words in a superword
python $wammar_utils/convert-closure-embeddings-to-word-embeddings.py -i $out/cluster_embeddings -o $out/embeddings

