import pytest
from unittest.mock import Mock, patch

from app.services.month_service import MonthService
from app.services.day_service import DayService
from app.services.solution_service import SolutionService
from app.core.exceptions import NotFoundError, ConflictError


class TestMonthService:
    def test_get_month_by_id_not_found(self, session):
        """Test getting a month that doesn't exist."""
        with pytest.raises(NotFoundError):
            MonthService.get_month_by_id(session, 999)

    def test_get_all_months(self, session):
        """Test getting all months."""
        # Seed data would be needed
        months = MonthService.get_all_months(session)
        assert isinstance(months, list)


class TestSolutionService:
    def test_get_solution_by_id_not_found(self, session):
        """Test getting a solution that doesn't exist."""
        with pytest.raises(NotFoundError):
            SolutionService.get_solution_by_id(session, 999)

    def test_create_solution_duplicate(self, session, sample_solution_data):
        """Test creating a duplicate solution."""
        # Create first solution
        SolutionService.create_solution(session, sample_solution_data)
        
        # Try to create duplicate
        with pytest.raises(ConflictError):
            SolutionService.create_solution(session, sample_solution_data)