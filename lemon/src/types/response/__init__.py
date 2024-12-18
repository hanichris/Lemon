from .data import Data, Generic, BaseModel, TypeVar, TypedDict
from .relationships import Relationship, RelationshipLinks, RelationshipKeys, Pick
from .params import Params
from .meta import Meta, MetaPage, MetaUrls
from .links import Links

D = TypeVar('D')
I = TypeVar('I')
M = TypeVar('M')
L = TypeVar('L')

class API(TypedDict):
    version: str

class LemonSqueezyResponse(BaseModel, Generic[D, L, M, I]):
    jsonapi: API
    links: L
    meta: M
    data: D
    included: list[I] | None = None