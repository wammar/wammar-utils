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
export monolingual_corpora="/usr1/home/wammar/monolingual/combo.bg /usr1/home/wammar/monolingual/combo.cs /usr1/home/wammar/monolingual/combo.da /usr1/home/wammar/monolingual/combo.de /usr1/home/wammar/monolingual/combo.el /usr1/home/wammar/monolingual/combo.en /usr1/home/wammar/monolingual/combo.es /usr1/home/wammar/monolingual/combo.fi /usr1/home/wammar/monolingual/combo.fr /usr1/home/wammar/monolingual/combo.hu /usr1/home/wammar/monolingual/combo.it /usr1/home/wammar/monolingual/combo.sv /usr1/home/wammar/monolingual/combo.af /usr1/home/wammar/monolingual/combo.ar /usr1/home/wammar/monolingual/combo.be /usr1/home/wammar/monolingual/combo.bn /usr1/home/wammar/monolingual/combo.bs /usr1/home/wammar/monolingual/combo.ca /usr1/home/wammar/monolingual/combo.ceb /usr1/home/wammar/monolingual/combo.cy /usr1/home/wammar/monolingual/combo.et /usr1/home/wammar/monolingual/combo.fa /usr1/home/wammar/monolingual/combo.ga /usr1/home/wammar/monolingual/combo.gl /usr1/home/wammar/monolingual/combo.gu /usr1/home/wammar/monolingual/combo.hi /usr1/home/wammar/monolingual/combo.hr /usr1/home/wammar/monolingual/combo.ht /usr1/home/wammar/monolingual/combo.hy /usr1/home/wammar/monolingual/combo.id /usr1/home/wammar/monolingual/combo.is /usr1/home/wammar/monolingual/combo.iw /usr1/home/wammar/monolingual/combo.ja /usr1/home/wammar/monolingual/combo.jw /usr1/home/wammar/monolingual/combo.ka /usr1/home/wammar/monolingual/combo.kk /usr1/home/wammar/monolingual/combo.kn /usr1/home/wammar/monolingual/combo.ko /usr1/home/wammar/monolingual/combo.la /usr1/home/wammar/monolingual/combo.lt /usr1/home/wammar/monolingual/combo.lv /usr1/home/wammar/monolingual/combo.mg /usr1/home/wammar/monolingual/combo.mi /usr1/home/wammar/monolingual/combo.mk /usr1/home/wammar/monolingual/combo.ml /usr1/home/wammar/monolingual/combo.mn /usr1/home/wammar/monolingual/combo.mr /usr1/home/wammar/monolingual/combo.ms /usr1/home/wammar/monolingual/combo.ne /usr1/home/wammar/monolingual/combo.nl /usr1/home/wammar/monolingual/combo.pl /usr1/home/wammar/monolingual/combo.pt /usr1/home/wammar/monolingual/combo.ro /usr1/home/wammar/monolingual/combo.ru /usr1/home/wammar/monolingual/combo.si /usr1/home/wammar/monolingual/combo.sl /usr1/home/wammar/monolingual/combo.so /usr1/home/wammar/monolingual/combo.sr /usr1/home/wammar/monolingual/combo.sw /usr1/home/wammar/monolingual/combo.ta /usr1/home/wammar/monolingual/combo.te /usr1/home/wammar/monolingual/combo.tg /usr1/home/wammar/monolingual/combo.tl /usr1/home/wammar/monolingual/combo.tr /usr1/home/wammar/monolingual/combo.uk /usr1/home/wammar/monolingual/combo.ur /usr1/home/wammar/monolingual/combo.uz /usr1/home/wammar/monolingual/combo.yi /usr1/home/wammar/monolingual/combo.zh /usr1/home/wammar/monolingual/combo.zu"

# space-delimited list of language prefixes. This list must be in the same order as the list of monolingual corpora.
export language_prefixes="bg: cs: da: de: el: en: es: fi: fr: hu: it: sv: af: ar: be: bn: bs: ca: ceb: cy: et: fa: ga: gl: gu: hi: hr: ht: hy: id: is: iw: ja: jw: ka: kk: kn: ko: la: lt: lv: mg: mi: mk: ml: mn: mr: ms: ne: nl: pl: pt: ro: ru: si: sl: so: sr: sw: ta: te: tg: tl: tr: uk: ur: uz: yi: zh: zu:"

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

