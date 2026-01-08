from typing import NoReturn


def fail() -> NoReturn:
    raise RuntimeError("boom")


def f(x: int) -> int:
    if x < 0:
        fail()
    else:
        return x

    return 0
