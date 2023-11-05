from datetime import datetime


def floattime_to_str(ft: float) -> str:
    ft = int(ft)
    s = ft % 60
    m = (ft // 60) % 60
    h = (ft // 3600) % 24
    d = ft // 86400

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


def floattime_to_datetime(ft: float) -> str:
    return datetime.fromtimestamp(ft).strftime("%Y年%m月%d日 %H時%M分%S秒")
