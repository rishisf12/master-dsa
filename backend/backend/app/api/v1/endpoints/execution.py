from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services.execution_service import ExecutionService
from app.utils.code_sanitizer import CodeSanitizer

router = APIRouter()


class ExecuteRequest(BaseModel):
    language: str  # "python" or "cpp"
    code: str
    stdin: Optional[str] = ""


@router.post("/execute")
async def execute_code(request: ExecuteRequest):
    """Execute Python or C++ code."""
    if request.language not in ["python", "cpp"]:
        raise HTTPException(status_code=400, detail="Language must be 'python' or 'cpp'")
    
    # Sanitize code before execution
    if request.language == "python":
        is_safe, message = CodeSanitizer.sanitize_python(request.code)
    else:
        is_safe, message = CodeSanitizer.sanitize_cpp(request.code)
    
    if not is_safe:
        raise HTTPException(status_code=400, detail=message)
    
    # Execute the code
    result = ExecutionService.execute(
        request.language,
        request.code,
        request.stdin
    )
    
    return {
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "returncode": result["returncode"]
    }