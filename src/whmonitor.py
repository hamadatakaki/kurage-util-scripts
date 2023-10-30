#!/usr/bin/env python3

import os
import whpost
import argparse
from dotenv import load_dotenv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    bot = whpost.BotWebHook(args)

    assert load_dotenv()
    user_id = os.environ.get("DISCORD_USER_ID")
    message = f"ドクター（ <@{user_id}> ）、監視していたプロセスがおわったよ。"
    bot.call_message(message)
