from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, List
from app.schemas.day import DayResponse


class MonthBase(SQLModel):
    name: str
    year: int
    month_number: int


class MonthCreate(MonthBase):
    pass


class MonthUpdate(SQLModel):
    name: Optional[str] = None
    year: Optional[int] = None
    month_number: Optional[int] = None


class MonthResponse(MonthBase):
    id: int
    created_at: datetime
    updated_at: datetime
    days: Optional[List[DayResponse]] = None

    class Config:
        from_attributes = True