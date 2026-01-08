from typing import TypedDict


class User(TypedDict):
    name: str
    age: int


user: User = {
    "name": "Alice"
    # missing "age"
}
