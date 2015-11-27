lang="bg"

wget http://download.wikimedia.org/${lang}wiki/latest/${lang}wiki-latest-pages-articles.xml.bz2
python WikiExtractor.py -cb 250K -o extracted-${lang} ${lang}wiki-latest-pages-articles.xml.bz2
find extracted-${lang} -name '*bz2' -exec bzip2 -c {} \; | egrep -v "^<" | egrep "." > wikipedia-${lang}.txt
rm -rf extracted-${lang}
