from typing import Any, ClassVar, Literal, NotRequired, TypedDict

from ..types.response import (
    RelationshipKeys,
    Data,
    LemonSqueezyResponse,
    MetaPage,
    Params,
    Pick,
)

type Events = Literal[
    "order_created",
    "order_refunded",
    "subscription_created",
    "subscription_updated",
    "subscription_cancelled",
    "subscription_resumed",
    "subscription_expired",
    "subscription_paused",
    "subscription_unpaused",
    "subscription_payment_success",
    "subscription_payment_failed",
    "subscription_payment_recovered",
    "subscription_payment_refunded",
    "license_key_created",
    "license_key_updated",
]

class StoreId(TypedDict, total=False):
    store_id: int | str

class NewWebhook(TypedDict):
    url: str
    events: list[Events]
    secret: str
    test_mode: NotRequired[bool]

class UpdateWebhook(TypedDict, total=False):
    url: str
    events: list[Events]
    secret: str

class Attributes(TypedDict):
    store_id: int
    url: str
    events: list[Events] | None
    last_sent_at: str | None
    created_at: str
    updated_at: str
    test_mode: bool

class WebhookData(
    Data[Attributes, Pick[RelationshipKeys](keys=['store']).pick()]
):
    pass

class GetWebhookParams(
    Params[list[Literal['store']], dict[str, Any]]
):
    filter: ClassVar
    page: ClassVar

class ListWebhookParams(
    Params[list[Literal['store']], StoreId]
):
    pass

Link = TypedDict('Link', {'self': str})
ListLink = TypedDict('ListLink', {'first': str, 'last': str})
Meta = TypedDict('Meta', {'page': MetaPage})

class Webhook(
    LemonSqueezyResponse[
        WebhookData,
        Link,
        Any,
        Data[dict[str, Any], Any]
    ]
):
    meta: ClassVar

    def __getitem__(self, item):
        return getattr(self, item)

class ListWebhooks(
    LemonSqueezyResponse[
        list[WebhookData],
        ListLink,
        Meta,
        Data[dict[str, Any], Any]
    ]
):
    pass