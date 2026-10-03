from sqlmodel import Session, select
from typing import List, Optional
from app.models.solution import Solution
from app.models.day import Day  # ✅ ADD THIS IMPORT
from app.core.exceptions import NotFoundError, ConflictError


class SolutionService:
    @staticmethod
    def get_solution_by_id(session: Session, solution_id: int) -> Solution:
        """Get a solution by ID."""
        solution = session.get(Solution, solution_id)
        if not solution:
            raise NotFoundError(f"Solution with ID {solution_id} not found")
        return solution

    @staticmethod
    def get_solutions_by_day(session: Session, day_id: int) -> List[Solution]:
        """Get all solutions for a specific day."""
        solutions = session.exec(
            select(Solution).where(Solution.day_id == day_id)
        ).all()
        return solutions

    @staticmethod
    def get_solution_by_day_and_problem(
        session: Session, 
        day_id: int, 
        problem_number: int
    ) -> Optional[Solution]:
        """Get a solution by day_id and problem_number."""
        solution = session.exec(
            select(Solution).where(
                Solution.day_id == day_id,
                Solution.problem_number == problem_number
            )
        ).first()
        return solution

    @staticmethod
    def create_solution(session: Session, solution_data: dict) -> Solution:
        """Create a new solution."""
        # ✅ ADD THIS CHECK: Verify day exists
        day = session.get(Day, solution_data["day_id"])
        if not day:
            raise NotFoundError(f"Day with ID {solution_data['day_id']} not found")
        
        # Check if solution already exists for this day and problem number
        existing = SolutionService.get_solution_by_day_and_problem(
            session, 
            solution_data["day_id"], 
            solution_data["problem_number"]
        )
        
        if existing:
            raise ConflictError(
                f"Solution for problem {solution_data['problem_number']} already exists for this day"
            )
        
        solution = Solution(**solution_data)
        session.add(solution)
        session.commit()
        session.refresh(solution)
        return solution

    @staticmethod
    def update_solution(session: Session, solution_id: int, solution_data: dict) -> Solution:
        """Update an existing solution."""
        if not solution_data:
            raise ValueError("No update data provided")
            
        solution = SolutionService.get_solution_by_id(session, solution_id)
        
        for key, value in solution_data.items():
            if value is not None:
                setattr(solution, key, value)
        
        session.add(solution)
        session.commit()
        session.refresh(solution)
        return solution

    @staticmethod
    def delete_solution(session: Session, solution_id: int) -> bool:
        """Delete a solution. Returns True if successful."""
        solution = SolutionService.get_solution_by_id(session, solution_id)
        session.delete(solution)
        session.commit()
        return True