#!/usr/bin/env python3

import os
import sys
import argparse
import json
import urllib.parse
import requests

from dotenv import load_dotenv


class BotWebHook(object):
    def __init__(self, args: argparse.Namespace):
        assert load_dotenv()

        self.url = os.environ.get("URL_POST_WEBHOOK")
        self.verbose = args.verbose

        if self.verbose:
            print(f"[verbose] POST to webhook: {self.url}")

        self.__check_environ()

    def __check_environ(self):
        url_parsed = urllib.parse.urlparse(self.url)
        if url_parsed.netloc != "discord.com":
            print("[error] Invalid WebHook URL")
            sys.exit(1)

    def call_message(self, message):
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (private use)",
        }
        content = {"content": message}
        data = json.dumps(content)

        res = requests.post(self.url, headers=headers, data=data)

        if self.verbose:
            print(f"[verbose] Response({res.status_code}): {res.content}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    bot = BotWebHook(args)
    bot.call_message(args.message)
