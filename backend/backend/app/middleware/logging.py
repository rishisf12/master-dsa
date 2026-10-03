import time
from fastapi import Request
from app.utils.logger import logger


async def logging_middleware(request: Request, call_next):
    """Log all incoming requests and their responses."""
    start_time = time.time()

    # Log request
    logger.info(f"→ {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"← {request.method} {request.url.path} "
        f"→ {response.status_code} "
        f"({process_time:.3f}s)"
    )

    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)

    return response