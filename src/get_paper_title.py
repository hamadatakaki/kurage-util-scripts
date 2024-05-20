#!/usr/bin/env python3

import argparse
import requests
import time
from bs4 import BeautifulSoup

def main(arxiv_id: str):
    time.sleep(0.5)
    res = requests.get(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")
    bs = BeautifulSoup(res.text, "xml")
    print(bs.feed.entry.title.string.replace("\n", ""), end="")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('id')
    parser.add_argument('--kind', default="arxiv")
    args = parser.parse_args()

    if (args.kind not in ["arxiv"]):
        raise ValueError(f"Undefined paper kind: '{args.kind}'")

    arxiv_id = args.id

    main(arxiv_id)
