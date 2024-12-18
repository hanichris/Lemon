from ..internal.request import fetch, FetchOptions, FetchResponse
from ..internal.utils import params_to_query_string, include_to_query_string
from .types import GetProductParams, ListProductParams, Product, ListProducts

async def get_product(
        product_id: int | str,
        params: dict = {}
):
    """Retrive the information about the provided product ID.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for the product with the given id.

    Args:
        `product_id`: The id of the product of interest.
        `params`: (Optional) Additional parameters.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error` and `status_code`. The
        `data` key holds the product object.

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature or if the LemonSqueezy API response doesn't match the provided
        pydantic schema.
    """
    options = FetchOptions(
        path=f"/v1/products/{product_id}",
        param=include_to_query_string(
            GetProductParams(**params).include
        )
    )
    return FetchResponse[Product](**await fetch(options)).model_dump()

async def list_products(params: dict = {}):
    """Retrieve a list of products.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for a list of products.

    Args:
        `params`: (Optional) Additional parameters.
        `params['filter']`: (Optional) Filter parameters.
        `params['filter']['store_id']`: (Optional) Only return products belonging
        to the store with this ID.
        `params['page']`: (Optional) Custom paginated queries.
        `params['page']['number']`: (Optional) The parameter determine which page
        to retrieve.
        `params['page']['size']`: (Optional) The parameter to determine how many
        results to return per page.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error`, and `status_code`. The
        `data` key holds the paginated list of product objects ordered by
        `created_at` (descending).

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature or if the LemonSqueezy API response doesn't match the provided
        pydantic schema.
    """
    options = FetchOptions(
        path="/v1/products",
        param=params_to_query_string(ListProductParams(**params))
    )
    return FetchResponse[ListProducts](**await fetch(options)).model_dump()