from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, List
from app.schemas.solution import SolutionResponse


class DayBase(SQLModel):
    date: datetime
    day_of_week: str
    week_number: int
    day_number: int
    month_id: int


class DayCreate(DayBase):
    pass


class DayUpdate(SQLModel):
    date: Optional[datetime] = None
    day_of_week: Optional[str] = None
    week_number: Optional[int] = None
    day_number: Optional[int] = None
    month_id: Optional[int] = None


class DayResponse(DayBase):
    id: int
    created_at: datetime
    updated_at: datetime
    solutions: Optional[List[SolutionResponse]] = None

    class Config:
        from_attributes = True