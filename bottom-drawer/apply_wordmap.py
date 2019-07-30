#!/usr/bin/env python3

def get_glues(style):
  #Returns (word-glue, morf-glue)
  if style == 'aff':
    return " ", "+ +"
  elif style == 'pre':
    return " ", " +"
  elif style == 'suf':
    return " ", "+ "
  elif style == 'wma':
    return " <w> ", " "
  else:
    raise ValueError("Unrecognized glue style: "+repr(style))

def read_and_preglue_wordmap(path, morf_glue):
  wordmap = {}
  with open(path) as fi:
    for line in fi:
      word, *morfs = line.strip().split()
      wordmap[word] = morf_glue.join(morfs)
  return wordmap

def apply_wordmap_and_glue(words, wordmap, word_glue):
  wordmapped = [wordmap[word] for word in words]
  return word_glue.join(wordmapped)

if __name__ == "__main__":
  import argparse, fileinput
  parser = argparse.ArgumentParser("Applies a Morfessor wordmap to a Kaldi-style text with different styles of glueing")
  parser.add_argument("wordmap")
  parser.add_argument("text")
  parser.add_argument("--glue-style", default="aff", choices=['aff','pre','suf','wma'], 
    help="The style of glue used: +aff+, +pre, suf+, <w> wma")
  args = parser.parse_args()
  word_glue, morf_glue = get_glues(args.glue_style)
  wordmap = read_and_preglue_wordmap(args.wordmap, morf_glue)
  for line in fileinput.input(args.text):
    uttid, *words = line.strip().split()
    mapped_and_glued = apply_wordmap_and_glue(words, wordmap, word_glue)
    print(uttid, mapped_and_glued)
