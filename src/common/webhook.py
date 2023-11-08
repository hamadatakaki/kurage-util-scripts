import json
import sys
import urllib.parse

import requests

import common.log


class Webhook(object):
    def __init__(self, url: str, verbose: bool = False, logger=None):
        self.url = url
        self.is_verbose = verbose
        self.logger = logger

        if self.is_verbose:
            common.log.verbose(f"webhook URL: {self.url}", file=self.logger)

        self.__check()

    def __call__(self, message: str):
        data = json.dumps({"content": message})
        res = requests.post(self.url, headers=self.headers, data=data)

        if self.is_verbose:
            common.log.verbose(
                f"Request: {message}",
                f"Response({res.status_code}): {res.content}",
                file=self.logger,
            )

    def __check(self):
        url_parsed = urllib.parse.urlparse(self.url)
        if url_parsed.netloc != "discord.com":
            common.log.error(f"Invalid WebHook URL: {self.url}", file=self.logger)
            sys.exit(1)

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "User-Agent": "Bot (private use)",
        }
