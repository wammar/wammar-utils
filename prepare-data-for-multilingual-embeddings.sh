#!/usr/bin/env bash
# author: waleed.ammar@gmail.com

echo "This script will use up ~1TB of disk space and will execute in ~2 days."

# copy bilingual dictionaries with forward * backward alignment probabilities, then filter out alignments with probability <= 0.25
for lang in bg cs da de el es fi fr hu it sv
do
  scp YOUR_USERNAME_HERE@allegro.clab.cs.cmu.edu:/usr3/home/wammar/corpora/parallel/word-alignment-based-bilingual-dicts/parallel.fwdxbwd-dict.${lang}-en align.${lang}-en
  awk '$3 > 0.25 {print $1,"|||",$2}' align.${lang}-en > dict.${lang}-en
done

# use 10 million sentences from the wikipedia dump of each language
for lang in bg cs da de el en es fi fr hu it sv
do
  wget http://download.wikimedia.org/${lang}wiki/latest/${lang}wiki-latest-pages-articles.xml.bz2
  python ~/wammar-utils/WikiExtractor.py --processes 1 -b 1G -o extracted-${lang} ${lang}wiki-latest-pages-articles.xml.bz2
  find extracted-${lang} -name 'wiki_*' -print0 | xargs -0 -I file cat file | egrep -v "^<" | egrep "." | ~/wammar-utils/europarl-tools/tokenizer.perl -l ${lang} | head -10000000 > mono.${lang}.cased
  python ~/wammar-utils/lowercase.py -i mono.${lang}.cased -o mono.${lang}

  # remove temporary files (uncomment the following line to save disk space)
  #rm -rf  mono.${lang}.cased extracted-${lang} ${lang}wiki-latest-pages-articles.xml.bz2
done

echo
echo "# Monolingual data:"
echo "ls mono.*"
echo
echo "# Bilingual dictionaries:"
echo "ls dict.*"
echo
echo "# Alignment probabilities:"
echo "ls align.*"
echo 
echo "# Now, please modify and execute the script that estimates multilingual embeddings: ~/wammar-utils/estimate-multilingual-embeddings.sh
