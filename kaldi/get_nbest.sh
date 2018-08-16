#!/bin/bash
set -eu -o pipefail

LMWT=13
num_best=50
cmd=run.pl

echo "$0 $@"  # Print the command line for logging
. ./path.sh
. parse_options.sh || exit 1;

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <graph|lang> <decode-dir>"
  exit 1
fi

lang_or_graph="$1"
dir="$2"
symtab="$lang_or_graph"/words.txt
outdir="$dir"/"$num_best"-best
mkdir -p "$outdir"

nj=$(cat "$dir"/num_jobs)

for f in "$symtab" "$dir"/lat.1.gz; do
  [ ! -f $f ] && echo "score.sh: no such file $f" && exit 1;
done

$cmd JOB=1:$nj "$outdir"/log/get_nbest.JOB.log \
  lattice-to-nbest --lm-scale="$LMWT" --n="$num_best" \
    "ark:gunzip -c $dir/lat.JOB.gz|" ark:- \| \
  nbest-to-linear ark:- ark:/dev/null \
    "ark,t:|int2sym.pl -f 2- $symtab > $outdir/text.JOB" || exit 1;

cat "$outdir"/text.* > "$outdir"/text && rm "$outdir"/text.*
echo "Done getting $num_best-best transcripts, output in $outdir"
