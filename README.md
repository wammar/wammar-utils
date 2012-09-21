wammar-utils
============

this repository is designed to be included as a submodule in other repositories


description of utilities:
===============
create-vocab.py
---------------
a python script that extracts the types in a text file and give them integer ids.
================
encode-corpus.py
----------------
a python script that replaces each type in the input file to a unique integer id in the target file. another file is output which contains the id:type mappings.
================
decode-corpus.py
----------------
inverse of encode-corpus.py.
=========================
filter-long-sent-pairs.py
-------------------------
a python script that filters out parallel sentences with number of tokens.
=========================
split-parallel-corpus.py
------------------------
a python script that splits a parallel corpus into train/dev/test sets.
