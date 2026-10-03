from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime, func


class Day(SQLModel, table=True):
    __tablename__ = "days"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    day_of_week: str
    week_number: int
    day_number: int
    month_id: int = Field(foreign_key="months.id")
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    # Relationships
    month: "Month" = Relationship(back_populates="days")
    solutions: List["Solution"] = Relationship(back_populates="day")