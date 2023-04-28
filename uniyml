#!/usr/bin/python3

import argparse
import yaml
import util

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", nargs="*")
    parser.add_argument("-d", "--dst")
    args = parser.parse_args()

    files = args.files
    dst = args.dst
    ymls = list()
    keys = list()

    for path in files:
        with open(path) as file:
            yml = yaml.safe_load(file)
            ymls.append(yml)
            keys.extend(list(yml.keys()))

    keys = list(set(keys))

    yml_dump = dict()

    for key in keys:
        yml_dump[key] = []
        for yml in ymls:
            if key in yml:
                yml_dump[key] += yml[key]

    with open(dst, "w") as file:
        yaml.dump(yml_dump, file, encoding="utf-8", allow_unicode=True)
