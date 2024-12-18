from typing import Generic, TypedDict, TypeVar

from pydantic import BaseModel, ConfigDict

from ..utils import Error, JSONAPIError
from ...types.response import API

T = TypeVar('T')

class HTTPStatusError(TypedDict, total=False):
    errors: list[JSONAPIError]
    jsonapi: API

class FetchResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status_code: int | None = None
    data: T | None | HTTPStatusError = None
    error: Error | None = None