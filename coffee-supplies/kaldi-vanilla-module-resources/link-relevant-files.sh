#!/bin/bash
#Run this in a Kaldi s5-style directory to install the relevant files (or actually links)
#needed to run Kaldi on Aalto Triton cluster
set -eu
relevant_files='path.sh cmd.sh conf/slurm.conf'

scriptdir=$(cd "$( dirname "$0" )" && pwd)

echo "Linking $relevant_files in $PWD"
echo "to $scriptdir"

mkdir -p "$PWD/conf"
for f in $relevant_files; do
  #symbolic link, force but create backup if exists
  ln -s -f -b "$scriptdir/$f" "$PWD/$f"
done
