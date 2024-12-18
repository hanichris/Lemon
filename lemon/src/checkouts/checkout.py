from ..internal.request import fetch, FetchOptions, FetchResponse, HTTPVerbEnum
from ..internal.utils import include_to_query_string, params_to_query_string
from .types import (
    Checkout,
    GetCheckoutParams,
    ListCheckoutParams,
    ListCheckouts,
    NewCheckout,
)

async def create_checkout(
    store_id: int | str,
    variant_id: int | str,
    checkout: NewCheckout = {}
):
    """Create a custom checkout URL for a specific variant.
    
    Makes a `POST` request to the LemonSqueezy API endpoint with data related to
    a new checkout request. Accompanying the request is the associated variant
    and store ids.
    See more: https://docs.lemonsqueezy.com/api/checkouts#create-a-checkout

    Args:
        `store_id`: The store to which a new checkout request is made.
        `variant_id`: The product variant of interest.
        `checkout`: A new checkout.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the checkout object created.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    relationships = {
        'store': {
            'data': {
                'type': 'stores',
                'id': str(store_id)
            }
        },
        'variant': {
            'data': {
                'type': 'variants',
                'id': str(variant_id)
            }
        },
    }

    attributes = {
        'custom_price': checkout.get('custom_price'),
        'expires_at': checkout.get('expires_at'),
        'preview': checkout.get('preview'),
        'test_mode': checkout.get('test_mode'),
        'product_options': checkout.get('product_options'),
        'checkout_options': checkout.get('checkout_options'),
        'checkout_data': checkout.get('checkout_data')
    }

    options = FetchOptions(
        path='/v1/checkouts',
        method=HTTPVerbEnum.POST,
        body={
            'data': {
                'type': 'checkouts',
                'attributes': attributes,
                'relationships': relationships,
            }
        }
    )
    return FetchResponse[Checkout](**await fetch(options)).model_dump()

async def get_checkout(checkout_id: int | str, params: dict = {}):
    """Retrieves a checkout.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for the checkout with the given id.

    Args:
        `checkout_id`: The checkout id.
        `params`: (Optional) Additional parameters.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the checkout object requested.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    options = FetchOptions(
        path=f"/v1/checkouts/{checkout_id}",
        param=include_to_query_string(
            GetCheckoutParams(**params).include
        )
    )
    return FetchResponse[Checkout](**await fetch(options)).model_dump()

async def list_checkouts(params: dict = {}):
    """Lists all checkouts.
    
    Args:
        `params`: (Optional) Additional parameters.
        `params['filter']`: (Optional) Filter parameters.
        `params['filter']['store_id']`: (Optional) Only return products belonging
        to the store with this ID.
        `params['filter']['variant_id']`: (Optional) Only return products
        belonging to the variant with this ID.
        `params['page']`: (Optional) Custom paginated queries.
        `params['page']['number']`: (Optional) The parameter determine which page
        to retrieve.
        `params['page']['size']`: (Optional) The parameter to determine how many
        results to return per page.
        `params['include']`: (Optional) Related resources.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the paginated list of checkout objects
        ordered by `created_at` (descending).
    """
    options = FetchOptions(
        path="/v1/checkouts",
        param=params_to_query_string(ListCheckoutParams(**params))
    )
    return FetchResponse[ListCheckouts](**await fetch(options)).model_dump()