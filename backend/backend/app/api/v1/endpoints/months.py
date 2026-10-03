from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.api.dependencies import get_db
from app.services.month_service import MonthService
from app.schemas.month import MonthResponse, MonthCreate


router = APIRouter()


@router.get("/months", response_model=List[MonthResponse])
async def get_months(session: Session = Depends(get_db)):
    """
    Get all months (August - November 2026).
    """
    months = MonthService.get_all_months(session)
    return months


@router.get("/months/{month_id}/days", response_model=List[dict])
async def get_month_days(month_id: int, session: Session = Depends(get_db)):
    """
    Get all days for a specific month.
    """
    month = MonthService.get_month_by_id(session, month_id)
    if not month:
        raise HTTPException(status_code=404, detail=f"Month {month_id} not found")
    
    # Return days with their solutions count
    days = []
    for day in month.days:
        days.append({
            "id": day.id,
            "date": day.date,
            "day_of_week": day.day_of_week,
            "week_number": day.week_number,
            "day_number": day.day_number,
            "solutions_count": len(day.solutions) if day.solutions else 0
        })
    
    return days


@router.post("/months", response_model=MonthResponse)
async def create_month(month_data: MonthCreate, session: Session = Depends(get_db)):
    """
    Create a new month (Admin only).
    """
    # Admin check should be added here
    month = MonthService.create_month(session, month_data.dict())
    return month