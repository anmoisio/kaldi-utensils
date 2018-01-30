#!/usr/bin/env python
# This script normalises a Kaldi format text file
from __future__ import print_function

try:
    import inflect
    found_inflect = True
except ImportError:
    found_inflect = False
import re
import os.path
import sys

def lettersOnly(text, keepid, case, convertnums):
    if keepid:
        splittext = text.split()
        idtokeep = splittext[0]
        try:
            text = " ".join(splittext[1:])
        except IndexError:
            text = ""
    if convertnums:
        if not found_inflect:
            print("Inflect not found, cannot convert numerals! Try: pip install inflect",
                file=sys.stderr)
        else:
            numconverter = inflect.engine().number_to_words
            #all numbers to words
            text = re.sub(r"(\d+(\.\d)+)", lambda s:numconverter(s,andword=''),text)
    #all whitespace to one space, and strip leading/trailing whitespace:
    text = re.sub(r"\s+"," ",text) 
    text = text.strip()
    #all non-unicode letters except spaces removed.
    text = re.sub(r"[^\w ]", "", text, flags=re.UNICODE)
    if case == "upper":
        text = text.upper()
    else:
        text = text.lower()
    if keepid:
        text = idtokeep+" "+text
    return text

if __name__ == "__main__":
    import argparse
    import fileinput
    parser = argparse.ArgumentParser("Normalise a kaldi format text file")
    parser.add_argument("--keepid",
            help = "Keep the first column as is, the uttid in a Kaldi format text file", 
            type = bool, default = True)
    parser.add_argument("--case", default = "upper", choices = ["upper", "lower"])
    parser.add_argument("--convertnums", 
            help="Convert numerals to words. Requires the inflect module.",
            type = bool, default=False)
    parser.add_argument("--encoding", default = "utf-8")
    parser.add_argument("files", nargs="*", help="Files to process. If empty, read from stdin.")
    args = parser.parse_args()
    for line in fileinput.input(files= args.files if args.files else "-"):
        processed = lettersOnly(line.decode(args.encoding),
                                keepid = args.keepid,
                                case = args.case,
                                convertnums = args.convertnums)
        print(processed.encode(args.encoding))
