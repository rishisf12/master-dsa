from sqlmodel import SQLModel
from typing import Optional


class AISummaryRequest(SQLModel):
    python_code: str
    cpp_code: str
    problem_name: str
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    notes: Optional[str] = None


class AISummaryResponse(SQLModel):
    summary: str
    generated_at: str