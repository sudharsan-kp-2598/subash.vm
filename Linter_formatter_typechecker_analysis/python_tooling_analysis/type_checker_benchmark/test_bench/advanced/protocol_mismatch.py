from typing import Protocol


class Writer(Protocol):
    def write(self, data: str) -> int:
        ...


class FileWriter:
    def write(self, data: bytes) -> int:  # wrong parameter type
        return len(data)


def save(w: Writer) -> int:
    return w.write("hello")


save(FileWriter())
