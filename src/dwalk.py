#!/usr/bin/env python3

import os
import sys
import argparse
from pathlib import Path

from common.path import has_extension, include_hidden


def parse_extension(ext: str) -> list[str]:
    if len(ext) == 0:
        return []
    elif "," in ext:
        return list([e.strip() for e in ext.split(",")])
    else:
        return [ext]


def main(args: argparse.Namespace):
    exts = parse_extension(args.extension)
    for r, _, fs in os.walk(args.top):
        for f in sorted(fs):
            p = Path(f"{r}/{f}")

            check_all = args.all or not include_hidden(p)
            if not check_all:
                continue

            check_exts = len(exts) == 0 or any(map(lambda e: has_extension(p, e), exts))
            if not check_exts:
                continue

            print(p)

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--extension", default="")
    parser.add_argument("-t", "--top", default=".")
    parser.add_argument("-a", "--all", action="store_true")
    args = parser.parse_args()

    sys.exit(main(args))
