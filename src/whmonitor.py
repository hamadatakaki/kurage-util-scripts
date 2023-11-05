#!/usr/bin/env python3

import os
import argparse
import psutil
import time
import threading
import queue
from dotenv import load_dotenv
from common.webhook import Webhook
from common.bot.monchan import Rosmontis


class ProcessMonitor(object):
    def __init__(
        self,
        pid: int,
        name: str,
        wh: Webhook,
        bot: Rosmontis,
        report_interval: int,
        check_interval: int,
    ):
        self.pid = pid
        self.name = name
        self.wh = wh
        self.bot = bot
        self.report_interval = report_interval
        self.check_interval = check_interval

    def track(self):
        t_start = time.time()
        share_queue = queue.Queue(maxsize=1)

        th_progress = threading.Thread(
            target=lambda: self.__progress(t_start, self.report_interval, share_queue),
            daemon=True,
        )
        th_check = threading.Thread(
            target=lambda: self.__check(t_start, self.check_interval, share_queue),
            daemon=True,
        )
        th_progress.start()
        th_check.start()

        th_check.join()
        th_progress.join()

        self.complete_report(t_start, time.time())

    def __check(self, t_start: float, interval: int, share_queue: queue.Queue):
        while True:
            ps = process_reference(self.pid)
            if ps == None:
                share_queue.put(True)
                break

            time_wait = interval - (time.time() - t_start) % interval
            time.sleep(time_wait)

    def __progress(self, t_start: float, interval: int, share_queue: queue.Queue):
        while True:
            if share_queue.full():
                break

            self.progress_report(t_start)
            time_wait = interval - (time.time() - t_start) % interval
            time.sleep(time_wait)

    def progress_report(self, t_start: float):
        ft = time.time() - t_start
        self.wh(self.bot.progress_report(self.name, ft))

    def complete_report(self, t_start: float, t_end: float):
        message = self.bot.complete_report(self.name)
        if t_end - t_start > 5:
            time_rep = self.bot.time_report(t_start, t_end)
            message = f"{message}\n{time_rep}"

        self.wh(message)


def process_reference(pid: int):
    if psutil.pid_exists(pid):
        return psutil.Process(pid)
    else:
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--name", default="プロセス")
    parser.add_argument("--pid")
    parser.add_argument("--report_interval", default=3600)
    parser.add_argument("--check_interval", default=5)
    args = parser.parse_args()

    assert load_dotenv()
    webhook_url = os.environ.get("URL_POST_WEBHOOK")
    user_id = os.environ.get("DISCORD_USER_ID")

    wh = Webhook(webhook_url)
    monchan = Rosmontis(user_id)

    if args.pid == None:
        message = monchan.complete_report(args.name)
        wh(message)
    else:
        monitor = ProcessMonitor(
            int(args.pid),
            args.name,
            wh,
            monchan,
            int(args.report_interval),
            int(args.check_interval),
        )
        monitor.track()
