from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import Column, DateTime, Text, JSON, func


class Notebook(SQLModel, table=True):
    __tablename__ = "notebooks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    cells: List[Dict[str, Any]] = Field(default=[], sa_column=Column(JSON))
    notebook_metadata: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_shared: bool = Field(default=False)
    share_link: Optional[str] = None
    day_id: int = Field(foreign_key="days.id")
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )
    
    # Relationships
    day: "Day" = Relationship()