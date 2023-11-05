def verbose(*objects, file=None):
    objs = list(map(lambda obj: f"[verbose] {obj}", objects))
    print(
        *objs,
        file=file,
        flush=True,
        sep="\n",
    )


def error(*objects, file=None):
    objs = list(map(lambda obj: f"[error] {obj}", objects))
    print(
        *objs,
        file=file,
        flush=True,
        sep="\n",
    )
