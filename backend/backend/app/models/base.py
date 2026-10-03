from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, func


class BaseModel(SQLModel):
    """
    Base model with common fields.
    This is a mixin - it does NOT create a table on its own.
    All other models inherit from this to get id, created_at, and updated_at.
    """
    
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    class Config:
        from_attributes = True