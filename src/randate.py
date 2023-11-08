#!/usr/bin/env python3

import argparse
import random
from datetime import datetime


def random_datestr():
    start = int(datetime(2015, 1, 1, 9, 0, 0).timestamp())
    end = int(datetime.now().timestamp())
    random_timestamp = random.randint(start, end)
    random_datetime = datetime.fromtimestamp(random_timestamp)

    return random_datetime.strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--n_uuid")
    args = parser.parse_args()
    n = int(args.n_uuid or 1)

    for _ in range(n):
        print(random_datestr())
