from typing import List


def add_item(items: List[object]) -> None:
    items.append("x")


strings: List[str] = ["a", "b"]

add_item(strings)  # List[str] is not List[object] (invariant)
