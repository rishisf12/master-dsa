from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.api.dependencies import get_db
from app.services.notebook_service import NotebookService
from app.services.execution_service import ExecutionService
from app.schemas.notebook import NotebookCreate, NotebookResponse, NotebookUpdate

router = APIRouter()
execution_service = ExecutionService()


@router.post("/notebooks", response_model=NotebookResponse)
async def create_notebook(notebook_data: NotebookCreate, session: Session = Depends(get_db)):
    """Create a new notebook."""
    notebook = NotebookService.create_notebook(session, notebook_data.dict())
    return notebook


@router.get("/notebooks/{notebook_id}", response_model=NotebookResponse)
async def get_notebook(notebook_id: int, session: Session = Depends(get_db)):
    """Get a notebook by ID."""
    notebook = NotebookService.get_notebook_by_id(session, notebook_id)
    return notebook


@router.put("/notebooks/{notebook_id}", response_model=NotebookResponse)
async def update_notebook(notebook_id: int, notebook_data: NotebookUpdate, session: Session = Depends(get_db)):
    """Update a notebook."""
    notebook = NotebookService.update_notebook(session, notebook_id, notebook_data.dict(exclude_unset=True))
    return notebook


@router.delete("/notebooks/{notebook_id}")
async def delete_notebook(notebook_id: int, session: Session = Depends(get_db)):
    """Delete a notebook."""
    NotebookService.delete_notebook(session, notebook_id)
    return {"message": f"Notebook {notebook_id} deleted successfully"}


@router.post("/notebooks/{notebook_id}/cells")
async def add_cell(notebook_id: int, cell_type: str, content: str, session: Session = Depends(get_db)):
    """Add a cell to a notebook."""
    notebook = NotebookService.add_cell(session, notebook_id, cell_type, content)
    return notebook


@router.put("/notebooks/{notebook_id}/cells/{cell_id}")
async def update_cell(notebook_id: int, cell_id: int, content: str, session: Session = Depends(get_db)):
    """Update a cell's content."""
    notebook = NotebookService.update_cell(session, notebook_id, cell_id, content)
    return notebook


@router.delete("/notebooks/{notebook_id}/cells/{cell_id}")
async def delete_cell(notebook_id: int, cell_id: int, session: Session = Depends(get_db)):
    """Delete a cell from a notebook."""
    notebook = NotebookService.delete_cell(session, notebook_id, cell_id)
    return notebook


@router.post("/notebooks/{notebook_id}/cells/{cell_id}/execute")
async def execute_cell(notebook_id: int, cell_id: int, session: Session = Depends(get_db)):
    """Execute a cell's code."""
    notebook = NotebookService.execute_cell(session, notebook_id, cell_id, execution_service)
    return notebook


@router.get("/notebooks/{notebook_id}/export")
async def export_notebook(notebook_id: int, format: str = "markdown", session: Session = Depends(get_db)):
    """Export a notebook in specified format."""
    notebook = NotebookService.get_notebook_by_id(session, notebook_id)
    
    if format == "markdown":
        from app.utils.notebook_utils import NotebookUtils
        markdown = NotebookUtils.export_to_markdown(notebook.__dict__)
        return {"content": markdown, "format": "markdown"}
    else:
        raise HTTPException(status_code=400, detail="Unsupported format. Use 'markdown'.")