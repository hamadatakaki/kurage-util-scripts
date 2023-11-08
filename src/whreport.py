#!/usr/bin/env python3

import os
import argparse
from dotenv import load_dotenv
from common.webhook import Webhook
from common.bot.monchan import Rosmontis


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--name", default="プロセス")
    args = parser.parse_args()

    assert load_dotenv()
    webhook_url = os.environ.get("URL_POST_WEBHOOK")
    user_id = os.environ.get("DISCORD_USER_ID")

    wh = Webhook(webhook_url, verbose=args.verbose)
    monchan = Rosmontis(user_id)
    message = monchan.complete_report(args.name)
    wh(message)
