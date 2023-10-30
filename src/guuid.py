#!/usr/bin/env python3

import argparse
import uuid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_uuid")
    parser.add_argument("-p", "--prefix")
    parser.add_argument("-s", "--suffix")
    args = parser.parse_args()

    n = int(args.n_uuid or 1)
    prefix = str(args.prefix or "")
    suffix = str(args.suffix or "")

    for _ in range(n):
        print(f"{prefix}{uuid.uuid4()}{suffix}")
