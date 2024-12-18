import sys

from enum import Enum
from typing import Any, cast, Generic, TypeVar

import httpx

from pydantic import BaseModel

from ..utils import get_kv, CONFIG_KEY, API_BASE_URL, Error, JSONAPIError


P = TypeVar('P')

class HTTPVerbEnum(str, Enum):
    GET     = "GET"
    POST    = "POST"
    DELETE  = "DELETE"
    PUT     = "PUT"
    PATCH   = "PATCH"


class FetchOptions(BaseModel, Generic[P]):
    path: str
    method: HTTPVerbEnum = HTTPVerbEnum.GET
    param: P | None = None
    body: dict[str, Any] | None = None


def create_lemon_error(
        message: str,
        cause: str | list[JSONAPIError] = "unknown"
) -> Error:
    error = Error(message)
    error.cause = cause
    return error


async def fetch(options: FetchOptions, requiresApiKey = True):
    """Customisation of request object.

    Utilises `httpx` internally to query the lemon squeezy api asynchronously.

    Args:
        options: options to pass to httpx. These include the `url`, `HTTP Verb`,
        `params` and request `body` if making a `POST` or `PATCH` request.
        requiresApiKey: boolean. Whether or not the api endpoint needs an
        accompanying api key to be sent with the request.

    Returns:
        Response: `dict`. Includes `status_code`, `data` and `error` as the keys
        to the response dictionary.
    
    Raises:
        `RuntimeError` if an error function is configured for lemon squeezy setup
        to raise a Runtime error when an erroneous object is generated.
    """
    options_valid = options.model_dump()
    response = {
        "status_code": None,
        "data": None,
        "error": cast(None | Error, None),
    }

    config: dict = cast(dict, get_kv(CONFIG_KEY))
    if config.get("api_key") is None:
        response["error"] = create_lemon_error(
            "Please provide your Lemon Squeezy API key. Create a new API key at "
            "`https://app.lemonsqueezy.com/settings/api`",
            "Missing API key"
        )
        # print(response["error"], file=sys.stderr)
        if (err_fn := config.get('on_error')):
            err_fn(response["error"])
        return response
    
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
    }

    if requiresApiKey:
        headers["Authorization"] = f"Bearer {config["api_key"]}"

    data = options.body if options.method in {"PATCH", "POST"} else None
    async with httpx.AsyncClient(
        base_url=API_BASE_URL,
        headers=headers,
        params=options_valid.get('param'),
        follow_redirects=True,
        timeout=None
    ) as client:
        try:
            match options.method:
                case HTTPVerbEnum.GET:
                    res = await client.get(options.path)
                case HTTPVerbEnum.POST:
                    res = await client.post(options.path, json=data)
                case HTTPVerbEnum.DELETE:
                    res = await client.delete(options.path)
                case HTTPVerbEnum.PATCH:
                    res = await client.patch(options.path, json=data)
                case _:
                    print("Unrecognised HTTP verb", file=sys.stderr)
                    response["error"] = create_lemon_error(
                        f"Unrecognised HTTP verb: {options.method}",
                        "unknown HTTP verb"
                    )
                    return response
            res.raise_for_status()
            response["status_code"] = res.status_code
            response["data"] = res.json() if res.status_code != 204 else None
        except httpx.RequestError as exc:
            response["error"] = create_lemon_error(
                f"{exc}", f"Error while requesting {exc.request.url!r}"
            )
            if (err_fn := config.get('on_error')):
                err_fn(response["error"])
        except httpx.HTTPStatusError as exc:
            _data = exc.response.json()
            _error = _data.get("errors") or \
            _data.get("error") or \
            _data.get("message") or "unknown cause"

            response["status_code"] = exc.response.status_code
            response["data"] = _data
            response["error"] = create_lemon_error(f"{exc}", _error)
            if (err_fn := config.get('on_error')):
                err_fn(response["error"])

    return response
