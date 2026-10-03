import pytest
from sqlmodel import Session, select

from app.models.month import Month
from app.models.day import Day
from app.models.solution import Solution


class TestDatabase:
    def test_month_crud(self, session):
        """Test Month CRUD operations."""
        # Create
        month = Month(name="August", year=2026, month_number=8)
        session.add(month)
        session.commit()
        session.refresh(month)
        
        assert month.id is not None
        
        # Read
        retrieved = session.get(Month, month.id)
        assert retrieved.name == "August"
        
        # Update
        retrieved.name = "September"
        session.add(retrieved)
        session.commit()
        
        updated = session.get(Month, month.id)
        assert updated.name == "September"
        
        # Delete
        session.delete(updated)
        session.commit()
        
        deleted = session.get(Month, month.id)
        assert deleted is None

    def test_solution_relationship(self, session):
        """Test Solution - Day relationship."""
        # Create day
        day = Day(
            date="2026-08-03",
            day_of_week="Monday",
            week_number=1,
            day_number=3,
            month_id=1
        )
        session.add(day)
        session.commit()
        session.refresh(day)
        
        # Create solution
        solution = Solution(
            problem_number=1,
            problem_name="Two Sum",
            difficulty="easy",
            day_id=day.id
        )
        session.add(solution)
        session.commit()
        
        # Verify relationship
        retrieved_day = session.get(Day, day.id)
        assert len(retrieved_day.solutions) == 1
        assert retrieved_day.solutions[0].problem_name == "Two Sum"