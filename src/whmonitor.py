#!/usr/bin/env python3

import os
import whpost
import argparse
from dotenv import load_dotenv
import psutil
import time
from datetime import datetime


def message_ja_timediff(td: float) -> str:
    td = int(td)
    s = td % 60
    m = td // 60
    h = td // 3600
    d = td // 86400

    if d > 0:
        return f"{d}日{h}時間{m}分{s}秒"
    else:
        if h > 0:
            return f"{h}時間{m}分{s}秒"
        else:
            if m > 0:
                return f"{m}分{s}秒"
            else:
                return f"{s}秒"


class ProcessMonitor(object):
    def __init__(self, args):
        self.process = psutil.Process(int(args.pid))
        self.bot = whpost.BotWebHook(args)
        self.th_elapsed = float(args.elapsed)

    def monitoring(self, user_id):
        start_ut = self.process.create_time()
        base_ut = start_ut
        s_process = f"プロセス（PID：{self.process.pid}）"

        while self.process.is_running():
            now_ut = time.time()

            if now_ut - base_ut > self.th_elapsed:
                base_ut = now_ut
                s_td = message_ja_timediff(now_ut - start_ut)
                msg = f"ドクター、{s_process}の監視を始めて{s_td}経過したよ。"
                self.bot.call_message(msg)

            time.sleep(10)

        now_ut = time.time()

        s_td = message_ja_timediff(now_ut - start_ut)
        s_start = datetime.fromtimestamp(start_ut).strftime("%y年%m月%d日 %H時%M分%S秒")
        s_now = datetime.fromtimestamp(now_ut).strftime("%y年%m月%d日 %H時%M分%S秒")
        msg_arr = [
            f"ドクター（ <@{user_id}> ）、監視していた{s_process}がおわったよ。",
            f"{s_start}に監視を始めて、{s_now}に監視をおわったよ。",
            f"その間にだいたい{s_td}くらい経過したよ。",
        ]
        self.bot.call_message("\n".join(msg_arr))


def no_pid_call(args, user_id):
    bot = whpost.BotWebHook(args)
    message = f"ドクター（ <@{user_id}> ）、監視していたプロセスがおわったよ。"
    bot.call_message(message)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--pid")
    parser.add_argument("--elapsed", default=3600)
    args = parser.parse_args()

    assert load_dotenv()
    user_id = os.environ.get("DISCORD_USER_ID")

    if args.pid == None:
        no_pid_call(args, user_id)
    else:
        monitor = ProcessMonitor(args)
        monitor.monitoring(user_id)
