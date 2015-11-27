export src_lang="de"
export tgt_lang="en"
export src_sents="20151028.de"
export tgt_sents="20151028.en"

# tokenize
../europarl-tools/tokenizer.perl -l $src_lang < $src_sents > $src_sents.tok
../europarl-tools/tokenizer.perl -l $tgt_lang < $tgt_sents > $tgt_sents.tok

# lowercase
tr '[:upper:]' '[:lower:]' < $src_sents.tok > $src_sents.tok.lower
tr '[:upper:]' '[:lower:]' < $tgt_sents.tok > $tgt_sents.tok.lower

# remove empty/long sentences and paste sentence pairs in the same file
python ~/wammar-utils/filter-long-sent-pairs.py -si $tgt_sents.tok.lower -so $tgt_sents.tok.lower.filter -ti $src_sents.tok.lower -to $src_sents.tok.lower.filter -sml 100 -tml 100
python ~/wammar-utils/paste.py -d ' ||| ' -i $src_sents.tok.lower.filter $tgt_sents.tok.lower.filter -o ${src_sents}__${tgt_sents}

# align and symmetrize
~/git/fast_align/fast_align -i ${src_sents}__${tgt_sents} -v -d -o -c ${src_sents}__${tgt_sents}.fastalignmodel > ${src_sents}__${tgt_sents}.fastalign
~/git/fast_align/fast_align -i ${src_sents}__${tgt_sents} -r -v -d -o -c ${src_sents}__${tgt_sents}.reversefastalignmodel > ${src_sents}__${tgt_sents}.reversefastalign
~/cdec/utils/atools -i ${src_sents}__${tgt_sents}.fastalign -j ${src_sents}__${tgt_sents}.reversefastalign -c intersect > ${src_sents}__${tgt_sents}.symfastalign
python ~/wammar-utils/alignments-to-dictionary.py -ip ${src_sents}__${tgt_sents} -ia ${src_sents}__${tgt_sents}.symfastalign -of ${src_sents}__${tgt_sents}.fwddict -ob ${src_sents}__${tgt_sents}.bwddict -op ${src_sents}__${tgt_sents}.dict

# cleanup
#rm $src_sents.tok $src_sents.tok.lower $src_sents.tok.lower.filter
#rm $tgt_sents.tok $tgt_sents.tok.lower $tgt_sents.tok.lower.filter
#rm ${src_sents}__${tgt_sents} ${src_sents}__${tgt_sents}.fastalign ${src_sents}__${tgt_sents}.reversefastalign ${src_sents}__${tgt_sents}.symfastalign

echo "dictionary can be found at ${src_sents}__${tgt_sents}.*dict"
