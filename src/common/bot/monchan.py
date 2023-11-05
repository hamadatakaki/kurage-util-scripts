import os

from dotenv import load_dotenv
from common.format import floattime_to_str, floattime_to_datetime


class Rosmontis(object):
    def __init__(self, doctor_id: str):
        self.doctor_id = doctor_id

    def doctor_name(self, mention=True) -> str:
        return f"ドクター（ <@{self.doctor_id}> ）" if mention else "ドクター"

    def progress_report(self, object: str, ft: float) -> str:
        message = f"{self.doctor_name(mention=False)}、{object}の監視を始めて{floattime_to_str(ft)}経過したよ。"
        return message

    def complete_report(self, object: str) -> str:
        message = f"{self.doctor_name()}、{object}の監視が終わったよ。"
        return message

    def time_report(self, ft_start: float, ft_end: float) -> str:
        s_start = floattime_to_datetime(ft_start)
        s_end = floattime_to_datetime(ft_end)
        s_dt = floattime_to_str(ft_end - ft_start)

        message = f"{s_start}に監視を始めて、{s_end}に監視をおわったよ。\nその間にだいたい{s_dt}くらい経過したよ。"
        return message