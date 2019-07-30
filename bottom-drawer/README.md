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

## normalise\_text.py
Normalises text, e.g. 
Shakespeare-37 Two beers...  or not 2 beers? 
-> Shakespeare-37 two beers or not two beers

## wer\_output\_filter\_finnish\_morf
Finnish text concatenator and fixer for Morfessor based output with any glueing mechanism.
Use something like this: `compute-wer ark:<ref> "ark:./wer_output_filter_finnish_morf <your hyp file> |"`
You can copy this file as local/wer_output_filter and Kaldi's scoring utilities will use it
