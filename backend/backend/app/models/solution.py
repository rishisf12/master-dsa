from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Text
from app.models.base import BaseModel


class Solution(BaseModel, table=True):
    __tablename__ = "solutions"
    
    problem_number: int = Field(ge=1, le=3)
    
    # Problem metadata
    problem_name: str
    problem_url: Optional[str] = None
    difficulty: str = Field(default="easy")
    pattern: Optional[str] = None
    
    # Solutions
    python_code: Optional[str] = Field(default=None, sa_column=Column(Text))
    cpp_code: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # ✅ Separate complexities for each language
    python_time_complexity: Optional[str] = None
    python_space_complexity: Optional[str] = None
    cpp_time_complexity: Optional[str] = None
    cpp_space_complexity: Optional[str] = None
    
    # Notes - shared
    notes: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # AI Analysis
    ai_summary: Optional[str] = Field(default=None, sa_column=Column(Text))
    ai_generated_at: Optional[datetime] = None
    
    # Status
    is_saved: bool = Field(default=False)
    is_complete: bool = Field(default=False)
    completed_at: Optional[datetime] = None
    
    # Foreign keys
    day_id: int = Field(foreign_key="days.id")
    
    # Relationships
    day: "Day" = Relationship(back_populates="solutions")