#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <dir-to-install-to>"
fi

dir="$1"

module load kaldi-vanilla
git clone github.com/kaldi/kaldi.git "$dir"
cd "$dir"
git checkout "$KALDI_COMMIT" #this is set by the module

