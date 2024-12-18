from typing import Any, TypedDict

class Links(TypedDict, total=False):
    about: str
    type: str

class Source(TypedDict, total=False):
    pointer: str
    parameter: str

class JSONAPIError(TypedDict, total=False):
    id: str
    links: Links
    status: str
    code: str
    title: str
    detail: str
    source: Source
    meta: dict[str, Any]


class Error:
    name = "Lemon Squeezy API Error"

    def __init__(self, message: str) -> None:
        self.message = message
    
    @property
    def message(self) -> str:
        return self._message
    
    @message.setter
    def message(self, value: str) -> None:
        self._message = value

    @property
    def cause(self) -> str | list[JSONAPIError]:
        return self._cause
    
    @cause.setter
    def cause(self, value: str | list[JSONAPIError]) -> None:
        self._cause = value

    def __repr__(self) -> str:
        return f"{self.name}: {self.message}"
