from typing import TypedDict, NotRequired


class Links(TypedDict):
    self: str
    first: str
    last: str
    next: NotRequired[str]
    prev: NotRequired[str]