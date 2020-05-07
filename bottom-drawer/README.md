## apply\_wordmap.py
Applies a Morfessor wordmap to a text, with different types of glueing:
    uttid1 an \<w\> app le
    uttid1 an app+ le
    uttid1 an app +le
    uttid1 an app+ +le

## generate\_random\_search\_args.py
Generate configs for random hyperparameter search, using a yaml format

## get\_nbest\_oracle\_text.sh
Finds the oracle (best) hypothesis out of the n best hypotheses. Outputs in text format.
For instance, if you are using a subword language model, you may need this hypothesis is text first, so that you can create the word level hypothesis and compare to a word level reference.

## modify\_root\_paths.sh
Modifies paths in text files, to change from one root path to another.
When you move a directory structure, and have absolute path references, the paths need to be changed to fix the references.

E.G. 

When you move /scratch/work/kaldi/egs/wsj/s5 -> /local/work/kaldi-trunk/egs/wsj/s5

You need to fix files such as data/train/feats.scp since it will still point to the old location


## normalise\_text.py
Normalises text, e.g. 
    Shakespeare-37 Two beers...  or not 2 beers? 
    -> Shakespeare-37 two beers or not two beers
