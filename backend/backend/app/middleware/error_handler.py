from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    NotFoundError, ValidationError, UnauthorizedError,
    ForbiddenError, ConflictError
)
from app.utils.logger import logger


async def error_handler_middleware(request: Request, call_next):
    """Global error handler middleware."""
    try:
        return await call_next(request)
    except NotFoundError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except ValidationError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except UnauthorizedError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except ForbiddenError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except ConflictError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )