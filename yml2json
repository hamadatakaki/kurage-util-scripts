#!/home/jellyfishrumble/.pyenv/shims/python3


import argparse
from pathlib import Path

from _yml2json import yml2json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("src")
    parser.add_argument("dst")

    args = parser.parse_args()

    src, dst = Path(args.src), Path(args.dst)

    assert src.exists()

    yml2json(src, dst)
