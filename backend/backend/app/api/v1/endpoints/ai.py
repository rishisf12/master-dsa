from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_db
from app.services.ai_service import AIService
from app.services.solution_service import SolutionService
from app.utils.logger import logger

router = APIRouter()
ai_service = AIService()


class AISummaryRequest(BaseModel):
    python_time_complexity: Optional[str] = None
    python_space_complexity: Optional[str] = None
    cpp_time_complexity: Optional[str] = None
    cpp_space_complexity: Optional[str] = None


@router.post("/solutions/{solution_id}/ai-summary")
async def generate_ai_summary(
    solution_id: int,
    request: AISummaryRequest,
    session: Session = Depends(get_db),
):
    """Generate AI summary for a solution comparing Python and C++ code."""
    try:
        logger.info(f"Generating AI summary for solution {solution_id}")
        
        # Get the solution
        solution = SolutionService.get_solution_by_id(session, solution_id)
        
        if not solution:
            raise HTTPException(status_code=404, detail=f"Solution {solution_id} not found")
        
        # Check if there's code to analyze
        if not solution.python_code and not solution.cpp_code:
            raise HTTPException(
                status_code=400, 
                detail="No code found to analyze. Please add Python or C++ code first."
            )
        
        logger.info(f"Solution {solution_id} found. Generating summary...")
        
        # ✅ Generate AI summary with separate TC/SC from request
        result = ai_service.generate_summary(
            problem_name=solution.problem_name or "Untitled Problem",
            python_code=solution.python_code or "# No Python code provided",
            cpp_code=solution.cpp_code or "// No C++ code provided",
            python_time_complexity=request.python_time_complexity,
            python_space_complexity=request.python_space_complexity,
            cpp_time_complexity=request.cpp_time_complexity,
            cpp_space_complexity=request.cpp_space_complexity,
            notes=solution.notes,
        )
        
        logger.info(f"AI result received: {result}")
        
        if result.get("error"):
            error_msg = result.get("summary", "Unknown AI error")
            logger.error(f"AI service returned error: {error_msg}")
            raise HTTPException(status_code=500, detail=f"AI generation failed: {error_msg}")
        
        # Save the AI summary to the solution
        solution.ai_summary = result["summary"]
        solution.ai_generated_at = datetime.now()
        session.add(solution)
        session.commit()
        session.refresh(solution)
        
        return {
            "summary": result["summary"],
            "generated_at": solution.ai_generated_at.isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"AI generation failed: {error_msg}")
        raise HTTPException(status_code=500, detail=f"AI generation failed: {error_msg}")