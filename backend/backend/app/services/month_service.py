from sqlmodel import Session, select
from app.models.month import Month
from app.models.day import Day
from app.core.exceptions import NotFoundError


class MonthService:
    @staticmethod
    def get_all_months(session: Session) -> list[Month]:
        """Get all months."""
        return session.exec(select(Month)).all()

    @staticmethod
    def get_month_by_id(session: Session, month_id: int) -> Month:
        """Get a month by ID."""
        month = session.get(Month, month_id)
        if not month:
            raise NotFoundError(f"Month with ID {month_id} not found")
        return month

    @staticmethod
    def get_month_days(session: Session, month_id: int) -> list[Day]:
        """Get all days for a specific month."""
        month = MonthService.get_month_by_id(session, month_id)
        return month.days

    @staticmethod
    def create_month(session: Session, month_data: dict) -> Month:
        """Create a new month."""
        month = Month(**month_data)
        session.add(month)
        session.commit()
        session.refresh(month)
        return month