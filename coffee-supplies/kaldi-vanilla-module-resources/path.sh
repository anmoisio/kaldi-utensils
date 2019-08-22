#!/bin/bash
#These are from the regular Kaldi path.sh
export LC_ALL=C
export PATH="$PWD/utils:$PWD:$PATH" #This needs to be placed in a kaldi s5-style directory, with utils, steps, conf etc. subdirectories

#Peter Smit (in AaltoASR Slack): 
#  "One important thing; limit the number of threads with `export OPENBLAS_NUM_THREADS=1` if you only have one thread available for the process"
#  "Otherwise it is really really really slow"
export OPENBLAS_NUM_THREADS=1

#Modules:
module load kaldi-vanilla
. $KALDI_ROOT/tools/config/common_path.sh
module load sox
module load Morfessor

#Misc:
export PYTHONIOENCODING='utf-8'
module list

[ -f ./local_path.sh ] && source local_path.sh
