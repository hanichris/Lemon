from typing import Generic, TypedDict, TypeVar

from pydantic import BaseModel


A = TypeVar('A')
R = TypeVar('R')

class Links(TypedDict):
    self: str

class Data(BaseModel, Generic[A, R]):
    type: str
    id: str
    attributes: A
    relationships: R
    links: Links
