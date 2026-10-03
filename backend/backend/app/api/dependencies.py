from fastapi import Depends
from sqlmodel import Session
from app.db.session import get_session


def get_db():
    """Get database session dependency."""
    session = next(get_session())
    try:
        yield session
    finally:
        session.close()


# Alias for get_db
SessionDep = Depends(get_db)