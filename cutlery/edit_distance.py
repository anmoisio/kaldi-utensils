#!/usr/bin/env python3
# Prints out edit distance between two Kaldi-style text files
# Very picky about input, their order and uttids need to match exactly
# Use sort text -o text (remember env LC_ALL=C for Kaldi conventions) and 
# utils/filter_scp.pl to make them match

#Implementation from:
#https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
def levenshtein(s1, s2):
  if len(s1) < len(s2):
    return levenshtein(s2, s1)
  # len(s1) >= len(s2)
  if len(s2) == 0:
    return len(s1)
  previous_row = range(len(s2) + 1)
  for i, c1 in enumerate(s1):
    current_row = [i + 1]
    for j, c2 in enumerate(s2):
      insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
      deletions = current_row[j] + 1     # than s2
      substitutions = previous_row[j] + (c1 != c2)
      current_row.append(min(insertions, deletions, substitutions))
    previous_row = current_row
  return previous_row[-1]

if __name__ == "__main__":
  import argparse
  import pathlib
  parser = argparse.ArgumentParser("""
    Compute Levenshtein distance for each entry in two kaldi-style text files.
    Make sure the texts are sorted in the same order and have exactly the same uttids.
    You can use utils/filter_scp.pl to filter any missing lines.""")
  parser.add_argument("texts", metavar="TEXT", nargs=2, type=pathlib.Path)
  args = parser.parse_args()
  with open(args.texts[0]) as fa, open(args.texts[1]) as fb:
    for line_a, line_b in zip(fa, fb):
      uttid_a, *text_a = line_a.strip().split()
      uttid_b, *text_b = line_b.strip().split()
      if uttid_a != uttid_b:
        raise ValueError("Utterances did not match exactly! Found out at: "+uttid_a+" != "+uttid_b)
      print(uttid_a, levenshtein(text_a, text_b))
  
