#!/bin/bash
# Use this script when you move a Kaldi-style s5 directory, which has absolute paths.

#These can be regular expressions, but escape ":"
source_path='/.*s5/' 
target_path=$(pwd)

. path.sh
. parse_options.sh

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <dir-root>"
  echo
  echo "Replaces all strings matching the --source_path option"
  echo "with the --target_path option"
  echo "in files under <dir-root> (or subdirectories)"
  echo "Options: "
  echo "  --source_path <source> #supports regexp, escape : (colon character)"
  echo "    default: '/.*s5/' #upto the s5 directory"
  echo "  --target_path <target> "
  echo "    default: fetch with pwd"
  exit 1
fi 

dir="$1"
nonbinary_files=$(find "$dir" -type f -exec grep -Iq . {} \; -print)

for f in $nonbinary_files; do
  sed -i -e "s:$source_path:$target_path/:g" "$f"
done
