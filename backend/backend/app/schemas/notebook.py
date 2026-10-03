from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional, List, Dict, Any


class NotebookBase(SQLModel):
    name: str
    description: Optional[str] = None
    day_id: int


class NotebookCreate(NotebookBase):
    cells: Optional[List[Dict[str, Any]]] = []
    notebook_metadata: Optional[Dict[str, Any]] = {}


class NotebookUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cells: Optional[List[Dict[str, Any]]] = None
    notebook_metadata: Optional[Dict[str, Any]] = None
    is_shared: Optional[bool] = None
    share_link: Optional[str] = None


class NotebookResponse(NotebookBase):
    id: int
    cells: List[Dict[str, Any]]
    notebook_metadata: Dict[str, Any]
    is_shared: bool
    share_link: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True