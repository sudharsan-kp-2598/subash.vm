from typing import List, Optional


def compute(values: List[int], flag: bool = True) -> Optional[int]:
    total = 0
    for v in values:
        if v % 2 == 0 and flag:
            total += v
        else:
            total += (
                v
                if v > 0
                else -v
            )
    return total if total > 10 else None


class Example:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f"Example(name={self.name!r})"
