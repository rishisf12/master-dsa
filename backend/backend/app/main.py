from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.db.session import engine
from app.models import Month, Day, Solution, Notebook
from app.api.v1.router import router
from app.middleware.error_handler import error_handler_middleware
from app.middleware.logging import logging_middleware
from app.utils.logger import logger
from sqlmodel import SQLModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    logger.info("Creating database tables...")
    SQLModel.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully!")
    yield
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Master DSA - Track your daily DSA practice with Python & C++",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ✅ CORS Middleware - ALLOW EVERYTHING (Development Only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← Change this to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom Middleware
app.middleware("http")(logging_middleware)
app.middleware("http")(error_handler_middleware)


# Include API Routes
app.include_router(router, prefix="/api/v1")


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "🚀 Master DSA API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )