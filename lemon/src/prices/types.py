from typing import Any, TypedDict, NotRequired, Literal, ClassVar

from ..types.response import (
    Data,
    LemonSqueezyResponse,
    MetaPage,
    Params,
    Pick,
    RelationshipKeys,
)

type Category = Literal["one_time", "subscription", "lead_magnet", "pwyw"]
type Scheme = Literal["standard", "package", "graduated", "volume"]
type UsageAggregation = Literal["sum", "last_during_period", "last_ever", "max"]
type TaxCode = Literal["eservice", "ebook", "saas"]

class Tier(TypedDict):
    last_unit: str | int
    unit_price: int
    unit_price_decimal: str | None
    fixed_fee: NotRequired[int]

class Attributes(TypedDict):
    variant_id: int
    category: Category
    scheme: Scheme
    usage_aggregation: UsageAggregation | None
    unit_price: int
    unit_price_decimal: str | None
    setup_fee_enabled: bool | None
    setup_fee: int | None
    package_size: int
    tiers: list[Tier] | None
    renewal_interval_unit: Literal["day", "week", "month", "year"] | None
    renewal_interval_quantity: int | None
    trial_interval_unit: Literal["day", "week", "month", "year"] | None
    trial_interval_quantity: int | None
    min_price: int | None
    suggested_price: None
    tax_code: TaxCode
    created_at: str
    updated_at: str


class VariantId(TypedDict):
    variant_id: NotRequired[int | str]

class PriceData(Data[Attributes, Pick[RelationshipKeys](keys=["variant"]).pick()]):
    pass

class GetPriceParams(Params[list[Literal['variant']], dict[str, Any]]):
    filter: ClassVar
    page: ClassVar

class ListPriceParams(Params[list[Literal['variant']], VariantId]):
    pass

Link = TypedDict('Link', {'self': str})
ListLink = TypedDict('ListLink', {'first': str, 'last': str})
Meta = TypedDict('Meta', {'page': MetaPage})

class Price(
    LemonSqueezyResponse[
        PriceData,
        Link,
        Any,
        Data[dict[str, Any], Any]
    ]
):
    meta: ClassVar


class ListPrices(
    LemonSqueezyResponse[
        list[PriceData],
        ListLink,
        Meta,
        Data[dict[str, Any], Any]
    ]
):
    pass