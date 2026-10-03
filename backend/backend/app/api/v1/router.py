from fastapi import APIRouter

from app.api.v1.endpoints import (
    months,
    days,
    solutions,
    execution,
    ai,
    auth,
    notebook,
)

router = APIRouter()

# Include all endpoint routers
router.include_router(months.router, tags=["months"])
router.include_router(days.router, tags=["days"])
router.include_router(solutions.router, tags=["solutions"])
router.include_router(execution.router, tags=["execution"])
router.include_router(ai.router, tags=["ai"])
router.include_router(auth.router, tags=["auth"])
router.include_router(notebook.router, tags=["notebook"])