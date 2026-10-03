from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.api.dependencies import get_db
from app.services.day_service import DayService
from app.schemas.day import DayResponse

router = APIRouter()


@router.get("/days/{day_id}", response_model=DayResponse)
async def get_day(day_id: int, session: Session = Depends(get_db)):
    """Get a specific day by ID."""
    day = DayService.get_day_by_id(session, day_id)
    return day


@router.get("/days/{day_id}/solutions")
async def get_day_solutions(day_id: int, session: Session = Depends(get_db)):
    """Get all solutions for a specific day."""
    day = DayService.get_day_by_id(session, day_id)
    solutions = []
    
    for solution in day.solutions:
        solutions.append({
            "id": solution.id,
            "problem_number": solution.problem_number,
            "problem_name": solution.problem_name,
            "difficulty": solution.difficulty,
            "is_saved": solution.is_saved,
            "is_complete": solution.is_complete,
        })
    
    return solutions


@router.get("/days/by-date/{date}")
async def get_day_by_date(date: str, session: Session = Depends(get_db)):
    """Get a day by date string (YYYY-MM-DD)."""
    day = DayService.get_day_by_date(session, date)
    return {
        "id": day.id,
        "date": day.date.isoformat(),
        "day_of_week": day.day_of_week,
        "week_number": day.week_number,
        "day_number": day.day_number,
    }