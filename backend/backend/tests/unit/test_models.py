import pytest
from datetime import datetime

from app.models.month import Month
from app.models.day import Day
from app.models.solution import Solution
from app.models.notebook import Notebook


class TestModels:
    def test_month_creation(self):
        """Test creating a Month model."""
        month = Month(
            name="August",
            year=2026,
            month_number=8
        )
        assert month.name == "August"
        assert month.year == 2026
        assert month.month_number == 8

    def test_day_creation(self):
        """Test creating a Day model."""
        day = Day(
            date=datetime(2026, 8, 3),
            day_of_week="Monday",
            week_number=1,
            day_number=3,
            month_id=1
        )
        assert day.day_of_week == "Monday"
        assert day.week_number == 1
        assert day.day_number == 3

    def test_solution_creation(self):
        """Test creating a Solution model."""
        solution = Solution(
            problem_number=1,
            problem_name="Two Sum",
            difficulty="easy",
            pattern="array",
            python_code="class Solution: pass",
            cpp_code="class Solution {};",
            time_complexity="O(n)",
            space_complexity="O(n)",
            notes="Hashmap approach",
            day_id=1
        )
        assert solution.problem_number == 1
        assert solution.problem_name == "Two Sum"
        assert solution.is_saved is False
        assert solution.is_complete is False

    def test_notebook_creation(self):
        """Test creating a Notebook model."""
        notebook = Notebook(
            name="My DSA Notebook",
            description="August 3, 2026",
            cells=[],
            metadata={},
            day_id=1
        )
        assert notebook.name == "My DSA Notebook"
        assert notebook.cells == []
        assert notebook.is_shared is False