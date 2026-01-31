import pytest
from datetime import datetime
from pydantic import ValidationError
from py_gamma_sdk.models import Market, PublicSearchMarket, parse_flexible_datetime

def test_market_model_validation():
    # Valid data
    valid_data = {
        "id": "1",
        "question": "Q",
        "conditionId": "0x1",
        "slug": "slug",
        "outcomes": ["A", "B"],
        "clobTokenIds": ["T1", "T2"]
    }
    market = Market(**valid_data)
    assert market.id == "1"

def test_market_model_invalid():
    # Missing required field
    invalid_data = {
        "id": "1",
        "question": "Q"
    }
    with pytest.raises(ValidationError):
        Market(**invalid_data)


class TestFlexibleDatetimeParsing:
    """Tests for the parse_flexible_datetime function."""

    def test_parse_none_returns_none(self):
        assert parse_flexible_datetime(None) is None

    def test_parse_datetime_returns_datetime(self):
        dt = datetime(2023, 4, 1, 12, 0, 0)
        assert parse_flexible_datetime(dt) is dt

    def test_parse_malformed_date_april(self):
        result = parse_flexible_datetime("AprilT1, 2023")
        assert isinstance(result, datetime)
        assert result == datetime(2023, 4, 1)

    def test_parse_malformed_date_march(self):
        result = parse_flexible_datetime("MarchT28, 2022")
        assert isinstance(result, datetime)
        assert result == datetime(2022, 3, 28)

    def test_parse_malformed_date_october(self):
        result = parse_flexible_datetime("OctoberT9, 2022")
        assert isinstance(result, datetime)
        assert result == datetime(2022, 10, 9)

    def test_parse_malformed_date_february(self):
        result = parse_flexible_datetime("FebruaryT27, 2022")
        assert isinstance(result, datetime)
        assert result == datetime(2022, 2, 27)

    def test_parse_malformed_date_case_insensitive(self):
        result = parse_flexible_datetime("MAYT8, 2022")
        assert isinstance(result, datetime)
        assert result == datetime(2022, 5, 8)

    def test_parse_malformed_date_with_space(self):
        """Test format like 'April 1, 2023' (space instead of T)."""
        result = parse_flexible_datetime("April 1, 2023")
        assert isinstance(result, datetime)
        assert result == datetime(2023, 4, 1)

    def test_parse_malformed_date_with_space_february(self):
        result = parse_flexible_datetime("February 27, 2022")
        assert isinstance(result, datetime)
        assert result == datetime(2022, 2, 27)

    def test_parse_space_instead_of_t_separator(self):
        result = parse_flexible_datetime("2026-01-30 19:37:52+00")
        assert result == "2026-01-30T19:37:52+00:00"

    def test_parse_truncated_positive_timezone(self):
        result = parse_flexible_datetime("2026-01-30T19:37:52+00")
        assert result == "2026-01-30T19:37:52+00:00"

    def test_parse_truncated_negative_timezone(self):
        result = parse_flexible_datetime("2026-01-30T19:37:52-00")
        assert result == "2026-01-30T19:37:52-00:00"


class TestPublicSearchMarketWithMalformedDate:
    """Tests for PublicSearchMarket model with malformed umaEndDate."""

    def test_parses_malformed_uma_end_date(self):
        data = {
            "id": "test-id",
            "question": "Test question?",
            "conditionId": "0x123",
            "slug": "test-slug",
            "umaEndDate": "AprilT1, 2023"
        }
        market = PublicSearchMarket(**data)
        assert market.uma_end_date == datetime(2023, 4, 1)

    def test_parses_standard_uma_end_date(self):
        data = {
            "id": "test-id",
            "question": "Test question?",
            "conditionId": "0x123",
            "slug": "test-slug",
            "umaEndDate": "2023-04-01T00:00:00"
        }
        market = PublicSearchMarket(**data)
        assert market.uma_end_date == datetime(2023, 4, 1, 0, 0, 0)

    def test_parses_uma_end_date_with_truncated_timezone(self):
        data = {
            "id": "test-id",
            "question": "Test question?",
            "conditionId": "0x123",
            "slug": "test-slug",
            "umaEndDate": "2023-04-01 12:00:00+00"
        }
        market = PublicSearchMarket(**data)
        assert market.uma_end_date is not None
