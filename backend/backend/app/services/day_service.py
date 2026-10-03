from sqlmodel import Session, select
from app.models.day import Day
from app.models.solution import Solution
from app.core.exceptions import NotFoundError
from datetime import datetime  # ✅ ADD THIS


class DayService:
    @staticmethod
    def get_day_by_id(session: Session, day_id: int) -> Day:
        """Get a day by ID."""
        day = session.get(Day, day_id)
        if not day:
            raise NotFoundError(f"Day with ID {day_id} not found")
        return day

    @staticmethod
    def get_day_solutions(session: Session, day_id: int) -> list[Solution]:
        """Get all solutions for a specific day."""
        day = DayService.get_day_by_id(session, day_id)
        return day.solutions

    @staticmethod
    def get_day_by_date(session: Session, date: str) -> Day:
        """Get a day by date string (YYYY-MM-DD)."""
        # ✅ Convert string to datetime
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise NotFoundError(f"Invalid date format: {date}")
        
        day = session.exec(
            select(Day).where(Day.date == date_obj)
        ).first()
        if not day:
            raise NotFoundError(f"Day with date {date} not found")
        return day