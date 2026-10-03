from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime, timedelta

from app.api.dependencies import get_db
from app.services.solution_service import SolutionService
from app.schemas.solution import SolutionCreate, SolutionResponse, SolutionUpdate
from app.models.solution import Solution
from app.models.day import Day

router = APIRouter()


# ✅ CREATE a solution
@router.post("/solutions", response_model=SolutionResponse)
async def create_solution(solution_data: SolutionCreate, session: Session = Depends(get_db)):
    """Create a new solution for a problem."""
    try:
        solution = SolutionService.create_solution(session, solution_data.dict())
        return solution
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET a specific solution by ID
@router.get("/solutions/{solution_id}", response_model=SolutionResponse)
async def get_solution(solution_id: int, session: Session = Depends(get_db)):
    """Get a specific solution by ID."""
    solution = SolutionService.get_solution_by_id(session, solution_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    return solution


# ✅ GET solutions by day_id (THIS WAS MISSING!)
@router.get("/days/{day_id}/solutions", response_model=List[SolutionResponse])
async def get_solutions_by_day(
    day_id: int, 
    session: Session = Depends(get_db)
):
    """Get all solutions for a specific day."""
    try:
        solutions = session.exec(
            select(Solution).where(Solution.day_id == day_id)
        ).all()
        return solutions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ GET solution by day_id and problem_number
@router.get("/solutions/by-day/{day_id}/problem/{problem_number}", response_model=SolutionResponse)
async def get_solution_by_day_and_problem(
    day_id: int, 
    problem_number: int, 
    session: Session = Depends(get_db)
):
    """Get a solution by day_id and problem_number."""
    solution = session.exec(
        select(Solution).where(
            Solution.day_id == day_id,
            Solution.problem_number == problem_number
        )
    ).first()
    
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    
    return solution


# ✅ UPDATE a solution
@router.put("/solutions/{solution_id}", response_model=SolutionResponse)
async def update_solution(
    solution_id: int, 
    solution_data: SolutionUpdate, 
    session: Session = Depends(get_db)
):
    """Update an existing solution."""
    solution = SolutionService.update_solution(session, solution_id, solution_data.dict(exclude_unset=True))
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    return solution


# ✅ DELETE a solution
@router.delete("/solutions/{solution_id}")
async def delete_solution(solution_id: int, session: Session = Depends(get_db)):
    """Delete a solution."""
    success = SolutionService.delete_solution(session, solution_id)
    if not success:
        raise HTTPException(status_code=404, detail="Solution not found")
    return {"message": f"Solution {solution_id} deleted successfully"}


# ✅ GET dashboard statistics
@router.get("/solutions/stats")
async def get_stats(session: Session = Depends(get_db)):
    """Get dashboard statistics: total, solved, streak."""
    try:
        # Total problems solved
        total = session.exec(select(Solution)).all()
        total_count = len(total)
        
        # Completed problems (is_complete = True)
        completed = session.exec(select(Solution).where(Solution.is_complete == True)).all()
        completed_count = len(completed)
        
        # Calculate streak (consecutive days with at least one solution)
        dates = session.exec(
            select(Day.date)
            .join(Solution)
            .distinct()
            .order_by(Day.date.desc())
        ).all()
        
        streak = 0
        if dates:
            today = datetime.now().date()
            expected_date = today
            
            for date_obj in dates:
                date_only = date_obj.date()
                if date_only == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                elif date_only < expected_date:
                    break
        
        return {
            "total": total_count,
            "solved": completed_count,
            "streak": streak
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))