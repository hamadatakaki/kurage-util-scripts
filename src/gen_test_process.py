import sys
import time
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", default=2)
    parser.add_argument("-e", "--exit_status", default=0)
    args = parser.parse_args()

    t = float(args.time)
    status = int(args.exit_status)

    time.sleep(t)
    sys.exit(status)
