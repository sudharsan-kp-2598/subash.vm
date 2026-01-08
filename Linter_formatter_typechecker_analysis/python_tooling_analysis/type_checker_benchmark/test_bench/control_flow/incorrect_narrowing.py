from typing import Union


def length(x: Union[str, int]) -> int:
    if isinstance(x, int):
        return len(x)
    else:
        return len(x)
