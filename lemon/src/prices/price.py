from ..internal.request import fetch, FetchOptions, FetchResponse
from ..internal.utils import params_to_query_string, include_to_query_string

from .types import GetPriceParams, ListPriceParams, Price, ListPrices

async def get_price(
        price_id: int | str,
        params: dict = {}
):
    """Retrive the information about the provided price ID.

    Makes a `GET` request with an optional set of path parameters
    to the lemonSqueezy API for the price with the given id.

    Args:
        `price_id`: The id of the price of interest.
        `params`: (Optional) Additional parameters.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error` and `status_code`. The
        `data` key holds the price object.

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature or if the LemonSqueezy API response doesn't match the provided
        pydantic schema.
    """
    options = FetchOptions(
        path=f"/v1/prices/{price_id}",
        param=include_to_query_string(
            GetPriceParams(**params).include
        )
    )
    return FetchResponse[Price](**await fetch(options)).model_dump()

async def list_prices(params: dict = {}):
    """Retrieve a list of prices.

    Makes a `GET` request with an optional set of path parameters
    to the lemonSqueezy API for a list of prices.

    Args:
        `params`: (Optional) Additional parameters.
        `params['filter']`: (Optional) Filter parameters.
        `params['filter']['variant_id']`: (Optional) Only return products
        belonging to the variant with this ID.
        `params['page']`: (Optional) Custom paginated queries.
        `params['page']['number']`: (Optional) The parameter determine which page
        to retrieve.
        `params['page']['size']`: (Optional) The parameter to determine how many
        results to return per page.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error`, and `status_code`. The
        `data` key holds the paginated list of price objects ordered by
        `created_at` (descending).

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature or if the LemonSqueezy API response doesn't match the provided
        pydantic schema.
    """
    options = FetchOptions(
        path="/v1/prices",
        param=params_to_query_string(ListPriceParams(**params))
    )
    return FetchResponse[ListPrices](**await fetch(options)).model_dump()