#!/bin/bash
set -eu -o pipefail

LMWT=13
num_best=50
cmd=run.pl
OOV="<UNK>"

echo "$0 $@"  # Print the command line for logging
. ./path.sh
. parse_options.sh || exit 1;

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <graph|lang> <decode-dir> <reference-text> <outdir>"
  exit 1
fi

lang_or_graph="$1"
dir="$2"
symtab="$lang_or_graph"/words.txt
reference="$3"
outdir="$4"
mkdir -p "$outdir"

nj=$(cat "$dir"/num_jobs)

for f in "$symtab" "$dir"/lat.1.gz; do
  [ ! -f $f ] && echo "$0: no such file $f" && exit 1;
done

#OOVID=$(grep "$OOV" $symtab | cut -d" " -f 2)

$cmd JOB=1:$nj "$outdir"/log/get_nbest_oracle_text.JOB.log \
  lattice-to-nbest --lm-scale="$LMWT" --n="$num_best" \
    "ark:gunzip -c $dir/lat.JOB.gz|" ark:- \| \
  nbest-to-lattice ark:- ark:- \| \
  lattice-oracle ark:- "ark,t:sym2int.pl -f 2- --map-oov '$OOV' $symtab <$reference |" \
    "ark,t:|int2sym.pl -f 2- $symtab > $outdir/text.JOB" || exit 1;

cat "$outdir"/text.* > "$outdir"/text && rm "$outdir"/text.*
