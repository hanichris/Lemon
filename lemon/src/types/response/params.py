from typing import TypedDict, NotRequired, Generic, TypeVar

from pydantic import BaseModel
I = TypeVar('I')
F = TypeVar('F')

class Page(TypedDict):
    number: NotRequired[int]
    size: NotRequired[int]

class Params(BaseModel, Generic[I, F]):
    include: I | None = None
    filter: F | None = None
    page: Page | None = None