import pytest
import respx
from httpx import Response
from pydantic import ValidationError
from py_gamma_sdk.models import (
    PublicSearchResponse,
    PublicSearchEvent,
    PublicSearchMarket,
)


VALID_MARKET = {
    "id": "1225133",
    "question": "Will Elon Musk post 0-19 tweets?",
    "conditionId": "0x94491b6c74801148fc60e613c1bb5fe187501a656148f051cdb57c1890195f27",
    "slug": "elon-musk-tweets-0-19",
    "active": True,
    "closed": False,
    "archived": False,
    "restricted": False,
    "new": False,
    "featured": True,
    "lastTradePrice": 0.5,
    "bestAsk": 0.51,
    "bestBid": 0.49,
    "volume": 100000.0,
    "liquidity": 50000.0,
}

VALID_EVENT = {
    "id": "175976",
    "slug": "elon-musk-tweets",
    "title": "Elon Musk # tweets January 23 - January 30, 2026?",
    "active": True,
    "closed": False,
    "archived": False,
    "new": False,
    "featured": True,
    "restricted": True,
    "volume": 20696371.968174,
    "liquidity": 2770021.05422,
    "markets": [VALID_MARKET],
}

VALID_RESPONSE = {"events": [VALID_EVENT]}


class TestPublicSearchMethod:
    """Test the public_search client method."""

    @pytest.mark.asyncio
    async def test_returns_typed_response(self, client):
        with respx.mock:
            respx.get("https://gamma-api.polymarket.com/public-search").mock(
                return_value=Response(200, json=VALID_RESPONSE)
            )
            result = await client.public_search("test")
            assert isinstance(result, PublicSearchResponse)
            assert isinstance(result.events[0], PublicSearchEvent)
            assert isinstance(result.events[0].markets[0], PublicSearchMarket)

    @pytest.mark.asyncio
    async def test_parses_event_fields(self, client):
        with respx.mock:
            respx.get("https://gamma-api.polymarket.com/public-search").mock(
                return_value=Response(200, json=VALID_RESPONSE)
            )
            result = await client.public_search("test")
            event = result.events[0]
            assert event.id == "175976"
            assert event.title == "Elon Musk # tweets January 23 - January 30, 2026?"
            assert event.volume == 20696371.968174
            assert event.active is True

    @pytest.mark.asyncio
    async def test_parses_market_fields(self, client):
        with respx.mock:
            respx.get("https://gamma-api.polymarket.com/public-search").mock(
                return_value=Response(200, json=VALID_RESPONSE)
            )
            result = await client.public_search("test")
            market = result.events[0].markets[0]
            assert market.id == "1225133"
            assert market.condition_id == "0x94491b6c74801148fc60e613c1bb5fe187501a656148f051cdb57c1890195f27"
            assert market.last_trade_price == 0.5

    @pytest.mark.asyncio
    async def test_empty_response(self, client):
        with respx.mock:
            respx.get("https://gamma-api.polymarket.com/public-search").mock(
                return_value=Response(200, json={"events": []})
            )
            result = await client.public_search("nonexistent")
            assert result.events == []


class TestPublicSearchMarketModel:
    """Test PublicSearchMarket model validation."""

    def test_valid_market(self):
        market = PublicSearchMarket(**VALID_MARKET)
        assert market.id == "1225133"
        assert market.condition_id == "0x94491b6c74801148fc60e613c1bb5fe187501a656148f051cdb57c1890195f27"

    def test_missing_required_field_id(self):
        invalid = {**VALID_MARKET}
        del invalid["id"]
        with pytest.raises(ValidationError):
            PublicSearchMarket(**invalid)

    def test_missing_required_field_question(self):
        invalid = {**VALID_MARKET}
        del invalid["question"]
        with pytest.raises(ValidationError):
            PublicSearchMarket(**invalid)

    def test_missing_required_field_condition_id(self):
        invalid = {**VALID_MARKET}
        del invalid["conditionId"]
        with pytest.raises(ValidationError):
            PublicSearchMarket(**invalid)

    def test_missing_required_field_slug(self):
        invalid = {**VALID_MARKET}
        del invalid["slug"]
        with pytest.raises(ValidationError):
            PublicSearchMarket(**invalid)

    def test_alias_field_mapping(self):
        market = PublicSearchMarket(**VALID_MARKET)
        assert market.last_trade_price == 0.5
        assert market.best_ask == 0.51
        assert market.best_bid == 0.49


class TestPublicSearchEventModel:
    """Test PublicSearchEvent model validation."""

    def test_valid_event(self):
        event = PublicSearchEvent(**VALID_EVENT)
        assert event.id == "175976"
        assert event.title == "Elon Musk # tweets January 23 - January 30, 2026?"

    def test_missing_required_field_id(self):
        invalid = {**VALID_EVENT}
        del invalid["id"]
        with pytest.raises(ValidationError):
            PublicSearchEvent(**invalid)

    def test_missing_required_field_slug(self):
        invalid = {**VALID_EVENT}
        del invalid["slug"]
        with pytest.raises(ValidationError):
            PublicSearchEvent(**invalid)

    def test_missing_required_field_title(self):
        invalid = {**VALID_EVENT}
        del invalid["title"]
        with pytest.raises(ValidationError):
            PublicSearchEvent(**invalid)

    def test_nested_markets_parsed(self):
        event = PublicSearchEvent(**VALID_EVENT)
        assert len(event.markets) == 1
        assert isinstance(event.markets[0], PublicSearchMarket)


class TestPublicSearchResponseModel:
    """Test PublicSearchResponse model validation."""

    def test_valid_response(self):
        response = PublicSearchResponse(**VALID_RESPONSE)
        assert len(response.events) == 1

    def test_empty_events(self):
        response = PublicSearchResponse(events=[])
        assert response.events == []

    def test_nested_structure_parsed(self):
        response = PublicSearchResponse(**VALID_RESPONSE)
        assert isinstance(response.events[0], PublicSearchEvent)
        assert isinstance(response.events[0].markets[0], PublicSearchMarket)
