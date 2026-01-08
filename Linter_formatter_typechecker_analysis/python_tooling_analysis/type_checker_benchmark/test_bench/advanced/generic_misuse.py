from typing import List


def total(values: List[int]) -> int:
    return sum(values)


numbers: List[str] = ["1", "2", "3"]

total(numbers)  # List[str] passed where List[int] is expected
