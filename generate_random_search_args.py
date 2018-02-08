#!/usr/bin/env python3
import random
import yaml
import os, os.path

def generateRandomConfig(template, float_format=".3f"):
    config = {}
    for key, value in template.items():
        if hasattr(value, "keys"): #Not a constant!
            raw_out = random.uniform(value["min"], value["max"])
            out_type = value.get("type", "float")
            if out_type == "int":
                out = format(int(raw_out))
            else:
                out = format(raw_out, float_format)
        else: #It's a constant
            out = format(value)
        config[key] = out
    return config

def readSlurmStyleIndices(string):
    ranges = string.strip().split(",")
    indices = []
    for r in ranges:
        if "-" in r:
            start, stop = map(int, r.split("-"))
            indices.extend(range(start, stop+1)) ##inclusive range
        else: ##it was just a single number
            indices.append(int(r))
    return indices
def indicesToFilepaths(indices, outdir):
    return [os.path.join(outdir, str(index)+".conf") for index in indices]

def readTemplate(filepath):
    #Reads the template from a YAML file. See argparse help below for format.
    with open(args.template, "r") as fi:
        return yaml.load(fi)
def writeConfig(config, filepath, value_separator=" ", separator=" "):
    with open(filepath, "w") as fo:
        for key, output in config.items():
            print(key, output, file=fo, sep=value_separator, end=separator)
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate configs for random hyperparameter search")
    parser.add_argument("template", help="""
        The config file template, in yaml notation.
        The keys are kept as they are.
        If the value is some constant, that is kept as is, too.
        If the value is a nested dict, the values are taken from uniform distribution between min and max attributes.
        If the value has 'type: int', the range is integer, otherwise real numbers. For constants, the type is automatically inferred.
        Example:
          --drop-out:
            min: 0.3
            max: 0.9
          --nlayers: 3
          --batch-size:
            min: 32
            max: 64
            type: int
        """)
    parser.add_argument("indices", help="Indices to use. This is in the Slurm array format: ranges are defined with dashes e.g. 3-5, and commas separate ranges/single values e.g. 7,29-49")
    parser.add_argument("outdir", help="Directory where to write output. Output files will be named <index>.conf, e.g. 23.conf")
    parser.add_argument("--value-separator", default=" ", help="Character that separates keys from values in the output. key1<value-separator>val1 key2<value-separator>val2")
    parser.add_argument("--separator", default=" ", help="Character that separates key-value pairs in the output. key1 val1<separator>key2 val2")
    parser.add_argument("--float-format", default=".3f", help="Output format for floats, in python format spec. Notably this specifies rounding.")
    args = parser.parse_args()

    ### Now run generate configs and write them out:
    try:
        os.makedirs(args.outdir)
    except FileExistsError:
        pass #Already there.
    template = readTemplate(args.template)
    indices = readSlurmStyleIndices(args.indices)
    for filepath in indicesToFilepaths(indices, args.outdir):
        conf = generateRandomConfig(template, float_format=args.float_format)
        writeConfig(conf, filepath)
