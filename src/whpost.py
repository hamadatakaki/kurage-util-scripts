#!/usr/bin/env python3

import os
import argparse

from dotenv import load_dotenv
from common.webhook import Webhook


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    assert load_dotenv()
    webhook_url = os.environ.get("URL_POST_WEBHOOK")

    bot = Webhook(webhook_url)
    bot(args.message)
