from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime, func


class Month(SQLModel, table=True):
    __tablename__ = "months"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    year: int
    month_number: int
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    # Relationships
    days: List["Day"] = Relationship(back_populates="month")