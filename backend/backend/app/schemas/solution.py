from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class SolutionBase(SQLModel):
    problem_number: int
    problem_name: str
    problem_url: Optional[str] = None
    difficulty: str = "easy"
    pattern: Optional[str] = None
    python_code: Optional[str] = None
    cpp_code: Optional[str] = None
    python_time_complexity: Optional[str] = None
    python_space_complexity: Optional[str] = None
    cpp_time_complexity: Optional[str] = None
    cpp_space_complexity: Optional[str] = None
    notes: Optional[str] = None
    day_id: int


class SolutionCreate(SolutionBase):
    # ✅ Add these fields that frontend sends
    is_saved: Optional[bool] = False
    is_complete: Optional[bool] = False


class SolutionUpdate(SQLModel):
    problem_number: Optional[int] = None
    problem_name: Optional[str] = None
    problem_url: Optional[str] = None
    difficulty: Optional[str] = None
    pattern: Optional[str] = None
    python_code: Optional[str] = None
    cpp_code: Optional[str] = None
    python_time_complexity: Optional[str] = None
    python_space_complexity: Optional[str] = None
    cpp_time_complexity: Optional[str] = None
    cpp_space_complexity: Optional[str] = None
    notes: Optional[str] = None
    is_saved: Optional[bool] = None
    is_complete: Optional[bool] = None
    completed_at: Optional[datetime] = None


class SolutionResponse(SolutionBase):
    id: int
    ai_summary: Optional[str] = None
    ai_generated_at: Optional[datetime] = None
    is_saved: bool
    is_complete: bool
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True