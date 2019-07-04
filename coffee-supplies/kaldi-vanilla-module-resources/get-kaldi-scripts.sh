#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <dir-to-install-to>"
  exit 1
fi

dir="$1"

module load kaldi-vanilla
git clone https://github.com/kaldi-asr/kaldi "$dir"
cd "$dir"
git checkout "$KALDI_COMMIT" #this is set by the module

