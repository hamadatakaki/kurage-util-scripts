#!/usr/bin/python3

import argparse
from datetime import datetime

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prefix")
    parser.add_argument("-s", "--suffix")
    parser.add_argument("-e", "--extension")
    args = parser.parse_args()

    pre = ""
    if args.prefix is not None:
        pre = str(args.prefix)

    ts = str(int(datetime.now().timestamp()))

    suf = ""
    if args.suffix is not None:
        suf = str(args.suffix)

    ext = str(args.extension or "txt")

    vec = [pre, ts, suf]
    name = "-".join(vec)

    print(f"{name}.{ext}")
