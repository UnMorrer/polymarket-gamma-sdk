from typing import List, Optional, Any, Union, Dict, Annotated
from pydantic import BaseModel, ConfigDict, Field, BeforeValidator
from datetime import datetime


def parse_flexible_datetime(value: Any) -> Any:
    """Parse datetime strings that may have non-standard formats."""
    if value is None or isinstance(value, datetime):
        return value
    if isinstance(value, str):
        # Handle format like '2026-01-30 19:37:52+00' -> '2026-01-30T19:37:52+00:00'
        if ' ' in value and 'T' not in value:
            value = value.replace(' ', 'T', 1)
        # Handle truncated timezone like '+00' -> '+00:00'
        if value.endswith('+00') or value.endswith('-00'):
            value = value + ':00'
    return value


FlexibleDatetime = Annotated[Optional[datetime], BeforeValidator(parse_flexible_datetime)]

class GammaBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

class Tag(GammaBaseModel):
    id: str
    label: Optional[str] = None
    slug: Optional[str] = None
    force_show: Optional[bool] = Field(None, alias="forceShow")
    force_hide: Optional[bool] = Field(None, alias="forceHide")
    is_carousel: Optional[bool] = Field(None, alias="isCarousel")
    published_at: Optional[str] = Field(None, alias="publishedAt")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class Market(GammaBaseModel):
    """Represents a single Polymarket market."""
    id: str
    question: str
    condition_id: str = Field(..., alias="conditionId")
    slug: str
    twitter_card_image: Optional[str] = Field(None, alias="twitterCardImage")
    resolution_source: Optional[str] = Field(None, alias="resolutionSource")
    end_date_iso: Optional[str] = Field(None, alias="endDateIso")
    category: Optional[str] = None
    amm_type: Optional[str] = Field(None, alias="ammType")
    liquidity: Optional[float] = None
    volume: Optional[float] = None
    outcomes: Union[List[str], str]
    clob_token_ids: Union[List[str], str] = Field(..., alias="clobTokenIds")
    group_item_title: Optional[str] = Field(None, alias="groupItemTitle")
    group_item_threshold: Optional[str] = Field(None, alias="groupItemThreshold")
    question_id: Optional[str] = Field(None, alias="questionId")
    rewards_min_size: Optional[float] = Field(None, alias="rewardsMinSize")
    rewards_max_spread: Optional[float] = Field(None, alias="rewardsMaxSpread")
    spread: Optional[float] = None
    last_trade_price: Optional[float] = Field(None, alias="lastTradePrice")
    best_bid: Optional[float] = Field(None, alias="bestBid")
    best_ask: Optional[float] = Field(None, alias="bestAsk")
    active: bool = True
    closed: bool = False
    archived: bool = False
    restricted: bool = False
    event_id: Optional[str] = Field(None, alias="eventId")

class Event(GammaBaseModel):
    """Represents an event that can contain multiple markets."""
    id: str
    ticker: Optional[str] = None
    slug: str
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    active: bool = True
    closed: bool = False
    archived: bool = False
    new: bool = False
    featured: bool = False
    restricted: bool = False
    start_date: Optional[datetime] = Field(None, alias="startDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    creation_date: Optional[datetime] = Field(None, alias="creationDate")
    last_updated_at: Optional[datetime] = Field(None, alias="lastUpdatedAt")
    markets: List[Market] = []
    tags: List[Tag] = []

class Team(GammaBaseModel):
    """Represents a sports team."""
    id: int
    name: str
    league: str
    record: Optional[str] = None
    logo: Optional[str] = None
    abbreviation: Optional[str] = None
    alias: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class SportMetadata(GammaBaseModel):
    """Provides metadata for sports events."""
    sport: str
    image: Optional[str] = None
    resolution: Optional[str] = None
    ordering: Optional[str] = None
    tags: Optional[str] = None
    series: Optional[str] = None

class Series(GammaBaseModel):
    """Represents a series or collection of events/markets."""
    id: str
    title: str
    slug: str
    active: bool
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class Comment(GammaBaseModel):
    """Represents a user comment on a market or event."""
    id: str
    comment: str
    user_address: str = Field(..., alias="userAddress")
    user_name: Optional[str] = Field(None, alias="userName")
    proxy_wallet: Optional[str] = Field(None, alias="proxyWallet")
    market_id: Optional[str] = Field(None, alias="marketId")
    event_id: Optional[str] = Field(None, alias="eventId")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

class Profile(GammaBaseModel):
    proxy_wallet: str = Field(..., alias="proxyWallet")
    display_name: Optional[str] = Field(None, alias="displayName")
    bio: Optional[str] = None
    image: Optional[str] = None
    created_at: Optional[datetime] = Field(None, alias="createdAt")


# ==========================================
# Public Search Response Models
# ==========================================

class PublicSearchMarket(GammaBaseModel):
    """Represents a market in the public search response."""
    id: str
    question: str
    condition_id: str = Field(..., alias="conditionId")
    slug: str
    resolution_source: Optional[str] = Field(None, alias="resolutionSource")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    start_date: Optional[datetime] = Field(None, alias="startDate")
    image: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    outcomes: Optional[str] = None
    outcome_prices: Optional[str] = Field(None, alias="outcomePrices")
    market_maker_address: Optional[str] = Field(None, alias="marketMakerAddress")
    closed_time: FlexibleDatetime = Field(None, alias="closedTime")
    submitted_by: Optional[str] = None
    resolved_by: Optional[str] = Field(None, alias="resolvedBy")
    group_item_title: Optional[str] = Field(None, alias="groupItemTitle")
    group_item_threshold: Optional[str] = Field(None, alias="groupItemThreshold")
    question_id: Optional[str] = Field(None, alias="questionID")
    uma_end_date: Optional[datetime] = Field(None, alias="umaEndDate")
    order_price_min_tick_size: Optional[float] = Field(None, alias="orderPriceMinTickSize")
    order_min_size: Optional[float] = Field(None, alias="orderMinSize")
    uma_resolution_status: Optional[str] = Field(None, alias="umaResolutionStatus")
    volume_num: Optional[float] = Field(None, alias="volumeNum")
    end_date_iso: Optional[str] = Field(None, alias="endDateIso")
    start_date_iso: Optional[str] = Field(None, alias="startDateIso")
    has_reviewed_dates: Optional[bool] = Field(None, alias="hasReviewedDates")
    clob_token_ids: Optional[str] = Field(None, alias="clobTokenIds")
    uma_bond: Optional[str] = Field(None, alias="umaBond")
    uma_reward: Optional[str] = Field(None, alias="umaReward")
    volume_1wk_clob: Optional[float] = Field(None, alias="volume1wkClob")
    volume_1mo_clob: Optional[float] = Field(None, alias="volume1moClob")
    volume_1yr_clob: Optional[float] = Field(None, alias="volume1yrClob")
    volume_clob: Optional[float] = Field(None, alias="volumeClob")
    custom_liveness: Optional[int] = Field(None, alias="customLiveness")
    accepting_orders: Optional[bool] = Field(None, alias="acceptingOrders")
    neg_risk_request_id: Optional[str] = Field(None, alias="negRiskRequestID")
    ready: Optional[bool] = None
    funded: Optional[bool] = None
    accepting_orders_timestamp: Optional[datetime] = Field(None, alias="acceptingOrdersTimestamp")
    cyom: Optional[bool] = None
    pager_duty_notification_enabled: Optional[bool] = Field(None, alias="pagerDutyNotificationEnabled")
    approved: Optional[bool] = None
    rewards_min_size: Optional[float] = Field(None, alias="rewardsMinSize")
    rewards_max_spread: Optional[float] = Field(None, alias="rewardsMaxSpread")
    spread: Optional[float] = None
    automatically_resolved: Optional[bool] = Field(None, alias="automaticallyResolved")
    last_trade_price: Optional[float] = Field(None, alias="lastTradePrice")
    best_ask: Optional[float] = Field(None, alias="bestAsk")
    best_bid: Optional[float] = Field(None, alias="bestBid")
    automatically_active: Optional[bool] = Field(None, alias="automaticallyActive")
    clear_book_on_start: Optional[bool] = Field(None, alias="clearBookOnStart")
    manual_activation: Optional[bool] = Field(None, alias="manualActivation")
    neg_risk_other: Optional[bool] = Field(None, alias="negRiskOther")
    uma_resolution_statuses: Optional[str] = Field(None, alias="umaResolutionStatuses")
    pending_deployment: Optional[bool] = Field(None, alias="pendingDeployment")
    deploying: Optional[bool] = None
    deploying_timestamp: Optional[datetime] = Field(None, alias="deployingTimestamp")
    rfq_enabled: Optional[bool] = Field(None, alias="rfqEnabled")
    holding_rewards_enabled: Optional[bool] = Field(None, alias="holdingRewardsEnabled")
    fees_enabled: Optional[bool] = Field(None, alias="feesEnabled")
    requires_translation: Optional[bool] = Field(None, alias="requiresTranslation")
    active: bool = True
    closed: bool = False
    archived: bool = False
    restricted: bool = False
    liquidity: Optional[float] = None
    volume: Optional[float] = None
    new: bool = False
    featured: bool = False
    neg_risk: Optional[bool] = Field(None, alias="negRisk")


class PublicSearchEvent(GammaBaseModel):
    """Represents an event in the public search response."""
    id: str
    ticker: Optional[str] = None
    slug: str
    title: str
    description: Optional[str] = None
    resolution_source: Optional[str] = Field(None, alias="resolutionSource")
    start_date: Optional[datetime] = Field(None, alias="startDate")
    creation_date: Optional[datetime] = Field(None, alias="creationDate")
    end_date: Optional[datetime] = Field(None, alias="endDate")
    image: Optional[str] = None
    icon: Optional[str] = None
    active: bool = True
    closed: bool = False
    archived: bool = False
    new: bool = False
    featured: bool = False
    restricted: bool = False
    liquidity: Optional[float] = None
    volume: Optional[float] = None
    open_interest: Optional[float] = Field(None, alias="openInterest")
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    competitive: Optional[float] = None
    volume_24hr: Optional[float] = Field(None, alias="volume24hr")
    volume_1wk: Optional[float] = Field(None, alias="volume1wk")
    volume_1mo: Optional[float] = Field(None, alias="volume1mo")
    volume_1yr: Optional[float] = Field(None, alias="volume1yr")
    enable_order_book: Optional[bool] = Field(None, alias="enableOrderBook")
    liquidity_clob: Optional[float] = Field(None, alias="liquidityClob")
    neg_risk: Optional[bool] = Field(None, alias="negRisk")
    neg_risk_market_id: Optional[str] = Field(None, alias="negRiskMarketID")
    comment_count: Optional[int] = Field(None, alias="commentCount")
    markets: List[PublicSearchMarket] = []


class PublicSearchResponse(GammaBaseModel):
    """Represents the response from the public search endpoint."""
    events: List[PublicSearchEvent] = []
    pagination: Optional[Dict[str, Any]] = None
