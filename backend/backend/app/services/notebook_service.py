from sqlmodel import Session, select
from app.models.notebook import Notebook
from app.core.exceptions import NotFoundError
from app.utils.notebook_utils import NotebookUtils


class NotebookService:
    @staticmethod
    def get_notebook_by_id(session: Session, notebook_id: int) -> Notebook:
        """Get a notebook by ID."""
        notebook = session.get(Notebook, notebook_id)
        if not notebook:
            raise NotFoundError(f"Notebook with ID {notebook_id} not found")
        return notebook

    @staticmethod
    def create_notebook(session: Session, notebook_data: dict) -> Notebook:
        """Create a new notebook."""
        empty_notebook = NotebookUtils.create_empty_notebook()
        notebook_data["cells"] = notebook_data.get("cells", empty_notebook["cells"])
        notebook_data["notebook_metadata"] = notebook_data.get("notebook_metadata", empty_notebook["metadata"])
        
        notebook = Notebook(**notebook_data)
        session.add(notebook)
        session.commit()
        session.refresh(notebook)
        return notebook

    @staticmethod
    def update_notebook(session: Session, notebook_id: int, notebook_data: dict) -> Notebook:
        """Update an existing notebook."""
        notebook = NotebookService.get_notebook_by_id(session, notebook_id)
        
        for key, value in notebook_data.items():
            if value is not None:
                setattr(notebook, key, value)
        
        session.add(notebook)
        session.commit()
        session.refresh(notebook)
        return notebook

    @staticmethod
    def delete_notebook(session: Session, notebook_id: int) -> None:
        """Delete a notebook."""
        notebook = NotebookService.get_notebook_by_id(session, notebook_id)
        session.delete(notebook)
        session.commit()

    @staticmethod
    def add_cell(session: Session, notebook_id: int, cell_type: str, content: str) -> Notebook:
        """Add a cell to a notebook."""
        notebook = NotebookService.get_notebook_by_id(session, notebook_id)
        cells = notebook.cells or []
        new_cell = {
            "id": len(cells) + 1,
            "type": cell_type,
            "content": content,
            "output": "",
            "status": "idle"
        }
        cells.append(new_cell)
        notebook.cells = cells
        session.add(notebook)
        session.commit()
        session.refresh(notebook)
        return notebook

    @staticmethod
    def update_cell(session: Session, notebook_id: int, cell_id: int, content: str) -> Notebook:
        """Update a cell's content."""
        notebook = NotebookService.get_notebook_by_id(session, notebook_id)
        cells = notebook.cells or []
        
        for cell in cells:
            if cell["id"] == cell_id:
                cell["content"] = content
                cell["output"] = ""
                cell["status"] = "idle"
                break
        
        notebook.cells = cells
        session.add(notebook)
        session.commit()
        session.refresh(notebook)
        return notebook

    @staticmethod
    def delete_cell(session: Session, notebook_id: int, cell_id: int) -> Notebook:
        """Delete a cell from a notebook."""
        notebook = NotebookService.get_notebook_by_id(session, notebook_id)
        cells = notebook.cells or []
        notebook.cells = [c for c in cells if c["id"] != cell_id]
        
        session.add(notebook)
        session.commit()
        session.refresh(notebook)
        return notebook

    @staticmethod
    def execute_cell(session: Session, notebook_id: int, cell_id: int, execution_service) -> Notebook:
        """Execute a cell's code."""
        notebook = NotebookService.get_notebook_by_id(session, notebook_id)
        cells = notebook.cells or []
        
        for cell in cells:
            if cell["id"] == cell_id:
                cell["status"] = "running"
                try:
                    result = execution_service.execute(
                        cell["type"],
                        cell["content"]
                    )
                    cell["output"] = result["stdout"] or result["stderr"]
                    cell["status"] = "success" if result["returncode"] == 0 else "error"
                except Exception as e:
                    cell["output"] = str(e)
                    cell["status"] = "error"
                break
        
        notebook.cells = cells
        session.add(notebook)
        session.commit()
        session.refresh(notebook)
        return notebook