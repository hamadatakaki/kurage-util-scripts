from pathlib import Path


def has_extension(path: Path, ext: str) -> bool:
    return str(path.suffix) == f".{ext}"


def include_hidden(path: Path) -> bool:
    if str(path) == ".":
        return False

    dirs = list(str(path).split("/"))
    has_hidden = any(map(lambda dname: len(dname) > 1 and dname.startswith("."), dirs))
    return has_hidden
