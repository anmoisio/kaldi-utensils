#!/usr/bin/env python3
# This script filters parallel texts by a simple length ratio heuristic.
# Also filters texts where either or both texts are empty.
# The idea is from: https://wit3.fbk.eu/papers/WIT3-EAMT2012.pdf
# Essentially: 
# "[P]airs of aligned [phrases] are marked as unreliable -- 
# if their length ratio is an outlier, assuming a normal distribution 
# and a 95% confidence interval"

# This script will work with Kaldi-style identifiers on the first column
# of the text files. For example:
# text.en:
# <uttid1> This is English
# text.swe:
# <uttid1> Den här är engelska

# The script will output a list of identifiers to REMOVE.
# Filter with e.g. the Kaldi utility: utils/filter_scp.pl --exclude
import pathlib
import statistics
from collections import namedtuple
import locale

def get_lengths(path):
  lengths = {}
  with open(path) as fi:
    for line in fi.readlines():
      uttid, *text = line.strip().split()
      lengths[uttid] = len(text)
  return lengths 

def find_zeros(lengths):
  return set(uttid for uttid, length in lengths.items() if length == 0)

def exclude(exclude_set, d):
  #Exclude keys from dict d
  return {key: val for key, val in d.items() if key not in exclude_set}

def get_length_ratios(lengths_a, lengths_b):
  return {uttid: length_a / lengths_b[uttid] for uttid, length_a in lengths_a.items()}

Bounds = namedtuple("Bounds", ["lower", "upper"])
def ratio_outlier_bounds(lenghts_ratios, cutoff = 1.96):
  #Cutoff is in standard deviations, 1.96 for 5% cutoff
  mean = statistics.mean(length_ratios.values())
  stddev = statistics.stdev(length_ratios.values())
  return Bounds(lower = mean-cutoff*stddev, upper = mean+cutoff*stddev)

def find_outlier_ratios(length_ratios, outlier_bounds):
  return set(uttid for uttid, ratio in length_ratios.items() if (
    ratio > outlier_bounds.upper or
    ratio < outlier_bounds.lower))

if __name__ == "__main__":
  import argparse
  import sys
  parser = argparse.ArgumentParser("""
    Filter parallel texts with a simple length ratio test. 
    Also filters uttids where at least one text is empty.
    Prints out a list of uttids to EXCLUDE.""")
  parser.add_argument("texts", nargs=2, type=pathlib.Path,
    help="""The text files to filter. 
      The format is to have ids on the first column.
      E.G.
      text.en:                    
      <uttid1> This is English
      text.swe:
      <uttid1> Den här är engelska""")
  parser.add_argument("--cutoff", type = float, default = 1.96,
      help = """Confidence interval cutoff in standard deviations. 
        1.96 for 5%, 2.58 for 1%, or look up in a table. 
        Not computed from a percentage to avoid dependencies.""")
  args = parser.parse_args() 
  #Read stuff 
  lengths_a, lengths_b = [get_lengths(path) for path in args.texts]
  #Filter out zero length utts
  zero_length_uttids = find_zeros(lengths_a) | find_zeros(lengths_b)
  lengths_a, lengths_b = [exclude(zero_length_uttids, l) for l in [lengths_a, lengths_b]]
  #Filter outlier length ratios
  length_ratios = get_length_ratios(lengths_a, lengths_b)
  outlier_bounds = ratio_outlier_bounds(length_ratios, cutoff = args.cutoff)
  print("Acceptable length ratio bounds:",
      "{bounds.lower:.3f} < ratio < {bounds.upper:.3f}".format(bounds=outlier_bounds), 
      file=sys.stderr)
  outlier_ratio_uttids = find_outlier_ratios(length_ratios, outlier_bounds)
  exclude_uttids = zero_length_uttids | outlier_ratio_uttids
  #Print the list of uttids to exclude
  print("Printing list of uttids to be excluded", file=sys.stderr)
  for uttid in sorted(exclude_uttids, key = locale.strxfrm):
    print(uttid)
