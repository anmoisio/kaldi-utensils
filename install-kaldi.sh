#!/bin/bash 
#This installs Kaldi on an Aalto desktop machine and should probably work for any Ubuntu 16.04 at least
#The pitfalls that this script should avoid:
# - g++ <5 needed for CUDA <=7.5, although we might soon get new CUDA versions after Spectre/Meltdown fix
# - Need certain packages which are not installed by default. This will ask for authentication, and you need to be
#   marked as a primary user of the computer you're installing on.
# - Use OpenBLAS, it is fast.

set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <install-dir>"
  echo " e.g. $0 kaldi-trunk to install here, at "$(pwd)/kaldi-trunk
  exit 1
fi

aptdcon --install "\
  autoconf
  automake
  g++-4.8
  gfortran-4.8
  liblapacke
  liblapacke-dev
  libopenblas-base
  libopenblas-dev
  libtool"


git clone https://github.com/kaldi-asr/kaldi.git
cd kaldi/tools
CXX=g++-4.8 extras/check_dependencies.sh
make -j4 CXX=g++-4.8 CC=gcc-4.8 FC=gfortran-4.8
cd ../src
CXX=g++-4.8 CC=gcc-4.8 ./configure --shared --mathlib=OPENBLAS --openblas-root=/usr/
make depend -j4 CXX=g++-4.8 CC=gcc-4.8
make -j4 CXX=g++-4.8 CC=gcc-4.8
