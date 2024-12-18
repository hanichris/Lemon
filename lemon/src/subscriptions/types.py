from typing import Any, ClassVar, Literal, NotRequired, TypedDict

from ..types.response import (
    RelationshipKeys,
    Data,
    LemonSqueezyResponse,
    MetaPage,
    Params,
    Pick
)

type SubscriptionStatus = Literal[
    "on_trial",
    "active",
    "paused",
    "pause",
    "past_due",
    "unpaid",
    "cancelled",
    "expired",
]

type CardBrand = Literal[
    "visa",
    "mastercard",
    "amex",
    "discover",
    "jcb",
    "diners",
    "unionpay",
]

class Pause(TypedDict):
    mode: Literal['void', 'free']
    resumes_at: NotRequired[str | None]

class FirstSubscriptionItem(TypedDict):
    id: int
    subscription_id: int
    price_id: int
    quantity: int
    is_usage_based: bool
    created_at: str
    updated_at: str

class Urls(TypedDict):
    update_payment_method: str
    customer_portal: str
    customer_portal_update_subscription: str

class UpdateSubscription(TypedDict, total=False):
    variant_id:int
    pause: Pause | None
    cancelled: bool
    trial_ends_at: str | None
    billing_anchor:int | None
    invoice_immediately: bool
    disable_prorations: bool

class Filter(TypedDict, total=False):
    store_id: str | int
    order_id: str | int
    order_item_id: str | int
    product_id: str | int
    variant_id: str | int
    user_email: str
    status: SubscriptionStatus

class Attributes(TypedDict):
    store_id: int
    customer_id: int
    order_id: int
    order_item_id: int
    product_id: int
    variant_id: int
    product_name: str
    variant_name: str
    user_name: str
    user_email: str
    status: SubscriptionStatus
    status_formatted: str
    card_brand: CardBrand | None
    card_last_four: str | None
    pause: Pause | None
    cancelled: bool
    trial_ends_at: str | None
    billing_anchor: int
    first_subscription_item: FirstSubscriptionItem | None
    urls: Urls
    renews_at: str
    ends_at: str | None
    created_at: str
    updated_at: str
    test_mode: bool


class SubscriptionData(
    Data[Attributes, Pick[RelationshipKeys](
        keys=[
            'store',
            'customer',
            'order',
            'order-item',
            'product',
            'variant',
            'subscription-items',
            'subscription-invoices',
        ]
    ).pick()]
):
    pass

class GetSubscriptionParams(
    Params[list[Literal[
        'store',
        'customer',
        'order',
        'order-item',
        'product',
        'variant',
        'subscription-items',
        'subscription-invoices',
    ]], dict[str, Any]]
):
    filter: ClassVar
    page: ClassVar

class ListSubscriptionParams(
    Params[list[Literal[
        'store',
        'customer',
        'order',
        'order-item',
        'product',
        'variant',
        'subscription-items',
        'subscription-invoices',
    ]], Filter]
):
    pass

Link = TypedDict('Link', {'self': str})
ListLink = TypedDict('ListLink', {'first': str, 'last': str})
Meta = TypedDict('Meta', {'page': MetaPage})

class Subscription(
    LemonSqueezyResponse[
        SubscriptionData,
        Link,
        Any,
        Data[dict[str, Any], Any]
    ]
):
    meta: ClassVar

class ListSubscriptions(
    LemonSqueezyResponse[
        list[SubscriptionData],
        ListLink,
        Meta,
        Data[dict[str, Any], Any]
    ]
):
    pass
