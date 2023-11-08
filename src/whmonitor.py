#!/usr/bin/env python3

import argparse
import os
import queue
import sys
import threading
import time

import psutil
from dotenv import load_dotenv

from common.bot.monchan import Rosmontis
from common.log import verbose
from common.webhook import Webhook


class NoProcessException(BaseException):
    pass


# TODO: checkが終了したときに強制的にprogressを行うような実装に修正


class ProcessMonitor(object):
    def __init__(
        self,
        pid: int,
        name: str,
        wh: Webhook,
        bot: Rosmontis,
        report_interval: int,
        check_interval: int,
        is_verbose: bool,
    ):
        ps = process_reference(pid)

        if ps == None:
            raise NoProcessException

        self.pid = pid
        self.name = name
        self.wh = wh
        self.bot = bot
        self.report_interval = report_interval
        self.check_interval = check_interval
        self.is_verbose = is_verbose

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

            if self.is_verbose:
                self.__verbose_check(ps == None)

            if ps == None:
                share_queue.put(True)
                break

            time_wait = interval - (time.time() - t_start) % interval
            time.sleep(time_wait)

    def __verbose_check(self, finished: bool):
        if finished:
            verbose(f"check: task `{self.name}` finished.")
        else:
            verbose(f"check: task `{self.name}` does not finish.")

    def __progress(self, t_start: float, interval: int, share_queue: queue.Queue):
        while True:
            cv_changed = share_queue.full()

            if self.is_verbose:
                self.__verbose_progress(cv_changed)

            if cv_changed:
                break

            self.progress_report(t_start)
            time_wait = interval - (time.time() - t_start) % interval
            time.sleep(time_wait)

    def __verbose_progress(self, finished: bool):
        if finished:
            verbose("progress: CV changed.")
        else:
            verbose("progress: CV does not change.")

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
    parser.add_argument("--pid", required=True)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--name", default="プロセス")
    parser.add_argument("--report_interval", default=3600)
    parser.add_argument("--check_interval", default=5)
    args = parser.parse_args()

    assert load_dotenv()
    webhook_url = os.environ.get("URL_POST_WEBHOOK")
    user_id = os.environ.get("DISCORD_USER_ID")

    wh = Webhook(webhook_url)
    monchan = Rosmontis(user_id)

    try:
        monitor = ProcessMonitor(
            int(args.pid),
            args.name,
            wh,
            monchan,
            int(args.report_interval),
            int(args.check_interval),
            args.verbose,
        )
        monitor.track()
    except NoProcessException:
        wh(monchan.no_object_report(f"{args.name}（PID: {args.pid}）"))
        sys.exit(1)
