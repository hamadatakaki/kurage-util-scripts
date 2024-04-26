#!/usr/bin/env python3

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("text")
    args = parser.parse_args()

    sanitized = args.text.replace(":", "").replace("\n", " ").replace(" ", "_")
    print(sanitized)
