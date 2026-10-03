import json
from typing import List, Dict, Any


class NotebookUtils:
    """Utility class for notebook operations."""
    
    @staticmethod
    def create_empty_notebook() -> Dict[str, Any]:
        """Create an empty notebook structure."""
        return {
            "cells": [],
            "metadata": {
                "created_at": None,
                "updated_at": None,
                "version": "1.0"
            }
        }
    
    @staticmethod
    def add_cell(notebook: Dict[str, Any], cell_type: str, content: str) -> Dict[str, Any]:
        """Add a new cell to the notebook."""
        cell = {
            "id": len(notebook["cells"]) + 1,
            "type": cell_type,  # "python", "cpp", "text"
            "content": content,
            "output": "",
            "status": "idle"  # "idle", "running", "success", "error"
        }
        notebook["cells"].append(cell)
        return notebook
    
    @staticmethod
    def update_cell(notebook: Dict[str, Any], cell_id: int, content: str) -> Dict[str, Any]:
        """Update a cell's content."""
        for cell in notebook["cells"]:
            if cell["id"] == cell_id:
                cell["content"] = content
                cell["output"] = ""
                cell["status"] = "idle"
                break
        return notebook
    
    @staticmethod
    def delete_cell(notebook: Dict[str, Any], cell_id: int) -> Dict[str, Any]:
        """Delete a cell from the notebook."""
        notebook["cells"] = [c for c in notebook["cells"] if c["id"] != cell_id]
        return notebook
    
    @staticmethod
    def move_cell(notebook: Dict[str, Any], cell_id: int, new_position: int) -> Dict[str, Any]:
        """Move a cell to a new position."""
        cells = notebook["cells"]
        for i, cell in enumerate(cells):
            if cell["id"] == cell_id:
                cell_obj = cells.pop(i)
                cells.insert(new_position, cell_obj)
                break
        return notebook
    
    @staticmethod
    def to_json(notebook: Dict[str, Any]) -> str:
        """Convert notebook to JSON string."""
        return json.dumps(notebook, indent=2)
    
    @staticmethod
    def from_json(json_str: str) -> Dict[str, Any]:
        """Load notebook from JSON string."""
        return json.loads(json_str)
    
    @staticmethod
    def export_to_markdown(notebook: Dict[str, Any]) -> str:
        """Export notebook to markdown format."""
        markdown = "# DSA Notebook\n\n"
        for cell in notebook["cells"]:
            if cell["type"] == "python":
                markdown += f"## Cell {cell['id']} (Python)\n\n```python\n{cell['content']}\n```\n\n"
                if cell["output"]:
                    markdown += f"**Output:**\n```\n{cell['output']}\n```\n\n"
            elif cell["type"] == "cpp":
                markdown += f"## Cell {cell['id']} (C++)\n\n```cpp\n{cell['content']}\n```\n\n"
                if cell["output"]:
                    markdown += f"**Output:**\n```\n{cell['output']}\n```\n\n"
            else:
                markdown += f"## Cell {cell['id']}\n\n{cell['content']}\n\n"
        return markdown