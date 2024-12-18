from ..internal.request import fetch, FetchOptions, FetchResponse, HTTPVerbEnum
from ..internal.utils import include_to_query_string, params_to_query_string
from .types import (
    GetWebhookParams,
    ListWebhooks,
    ListWebhookParams,
    NewWebhook,
    UpdateWebhook,
    Webhook
)

async def create_webhook(store_id: str | int, webhook: NewWebhook):
    """Create a webhook.

    Makes a `POST` request to the LemonSqueezy API endpoint with data related to
    a new webhook request. Accompanying the request is the associated store id.

    Args:
        `store_id`: The store to which the new webhook request is made.
        `webhook`: New webhook information.

    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the webhook object created.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    relationship = {
        'store': {
            'data': {
                'type': 'stores',
                'id': str(store_id)
            },
        },
    }
    attributes = {
        'url': webhook.get('url'),
        'events': webhook.get('events'),
        'secret': webhook.get('secret'),
        'test_mode': webhook.get('test_mode'),
    }

    options = FetchOptions(
        path='/v1/webhooks',
        method=HTTPVerbEnum.POST,
        body={
            'data': {
                'type': 'webhooks',
                'attributes': attributes,
                'relationships': relationship
            }
        }

    )
    return FetchResponse[Webhook](**await fetch(options)).model_dump()

async def get_webhook(webhook_id: str | int, params = {}):
    """Retrieve a webhook.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for the webhook with the given id.

    Args:
        `webhook_id`: The given webhook id.
        `params`: (Optional) Additional parameters.
        `params['include']`: (Optional) Related resources.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the webhook object requested.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    options = FetchOptions(
        path=f"/v1/webhooks/{webhook_id}",
        param=include_to_query_string(
            GetWebhookParams(**params).include
        )
    )
    return FetchResponse[Webhook](**await fetch(options)).model_dump()


async def update_webhook(webhook_id: str | int, webhook: UpdateWebhook):
    """Update a webhook.

    Makes a `PATCH` request with a set of parameters encoding the information to
    update lemonSqueezy API pertaining to a given webhook identified with the
    provided id.

    Args:
        `webhook_id`: The webhook id.
        `webhook`: The webhook information to update.
    
    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `data` key holds the value of the updated webhook object.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    attributes = {
        'url': webhook.get('url'),
        'events': webhook.get('events'),
        'secret': webhook.get('secret'),
    }

    options = FetchOptions(
        path=f"/v1/webhooks/{webhook_id}",
        method=HTTPVerbEnum.PATCH,
        body={
            'data': {
                'id': str(webhook_id),
                'type': 'webhooks',
                'attributes': attributes,
            },
        }
    )
    return FetchResponse[Webhook](**await fetch(options)).model_dump()

async def delete_webhook(webhook_id: str | int):
    """Delete a webhook.

    Args:
        `webhook_id`: The webhook id.

    Returns:
        Response object with the keys `data`, `error` and `status_code`.
        The `status_code` will be 204.

    Raises:
        `ValidationError`: If the parameters or response do not match the expected
        pydantic schemas.
    """
    options = FetchOptions(
        path=f"/v1/webhooks/{webhook_id}",
        method=HTTPVerbEnum.DELETE
    )

    return FetchResponse(**await fetch(options)).model_dump()

async def list_webhooks(params = {}):
    """Retrieve a list of webhooks.

    Makes a `GET` request with an optional set of path parameters to the
    lemonSqueezy API for a list of webhooks.

    Args:
        `params`: (Optional) Additional parameters.
        `params['filter']`: (Optional) Filter parameters.
        `params['filter']['store_id']`: (Optional) Only return webhooks
        belonging to the store with this ID.
        `params['page']`: (Optional) Custom paginated queries.
        `params['page']['number']`: (Optional) The parameter determine which page
        to retrieve.
        `params['page']['size']`: (Optional) The parameter to determine how many
        results to return per page.
        `params['include']`: (Optional) Related resources.

    Returns:
        Response object with the keys `data`, `error`, and `status_code`. The
        `data` key holds the paginated list of webhook objects ordered by
        `created_at` (descending).

    Raises:
        ValidationError: If the parameters passed do not match the required
        signature or if the LemonSqueezy API response doesn't match the provided
        pydantic schema.
    """
    options = FetchOptions(
        path='/v1/webhooks',
        param=params_to_query_string(ListWebhookParams(**params))
    )
    return FetchResponse[ListWebhooks](**await fetch(options)).model_dump()