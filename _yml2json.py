from pathlib import Path
import yaml
from datetime import datetime


def custom_dump(obj) -> str:
    if isinstance(obj, dict):
        lines = [f"{key}: {custom_dump(value)}" for key, value in obj.items()]
        return "{%s}" % ",\n".join(lines)
    if isinstance(obj, list):
        lines = [custom_dump(value) for value in obj]
        return "[%s]" % ",\n".join(lines)
    if isinstance(obj, datetime):
        return "new Date('%s')" % obj.strftime("%Y-%m-%d %H:%M:%S+09")
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, int):
        return obj

    return '"%s"' % str(obj)


def yml2json(src: Path, dst: Path):
    with open(src) as src:
        data = yaml.safe_load(src)

    with open(dst, "w") as dst:
        data = custom_dump(data)
        dst.write(data)
