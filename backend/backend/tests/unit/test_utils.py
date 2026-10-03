import pytest

from app.utils.validators import validate_url, validate_complexity, validate_code
from app.utils.date_utils import get_month_days, get_week_number, format_date


class TestValidators:
    def test_validate_url_valid(self):
        """Test valid URLs."""
        assert validate_url("https://leetcode.com/problems/two-sum/") is True
        assert validate_url("http://localhost:8000") is True

    def test_validate_url_invalid(self):
        """Test invalid URLs."""
        assert validate_url("not-a-url") is False
        assert validate_url("") is True  # Empty is allowed

    def test_validate_complexity_valid(self):
        """Test valid complexity formats."""
        assert validate_complexity("O(n)") is True
        assert validate_complexity("O(log n)") is True
        assert validate_complexity("O(n^2)") is True

    def test_validate_complexity_invalid(self):
        """Test invalid complexity formats."""
        assert validate_complexity("n") is False
        assert validate_complexity("O(n") is False

    def test_validate_code(self):
        """Test code validation."""
        assert validate_code("print('Hello')") is True
        assert validate_code("") is False
        assert validate_code(None) is False


class TestDateUtils:
    def test_get_month_days(self):
        """Test getting days in a month."""
        days = get_month_days(2026, 8)  # August
        assert len(days) == 31

    def test_get_week_number(self):
        """Test getting week number."""
        from datetime import datetime
        date = datetime(2026, 8, 3)
        week = get_week_number(date)
        assert week == 1

    def test_format_date(self):
        """Test date formatting."""
        from datetime import datetime
        date = datetime(2026, 8, 3)
        assert format_date(date) == "2026-08-03"