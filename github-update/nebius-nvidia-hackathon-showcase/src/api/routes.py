"""API routes for the hackathon project."""

import time
import uuid
from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from prometheus_client import Counter, Histogram, generate_latest
from pydantic import BaseModel, Field

from src.core.config import get_app_settings, get_settings
from src.core.logging import configure_logging, get_logger
from src.models.nim_client import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    EmbeddingRequest,
    EmbeddingResponse,
    MockNIMClient,
    NIMChatClient,
    NIMEmbeddingClient,
    NIMRerankClient,
    RerankRequest,
    RerankResponse,
    get_chat_client,
    get_embedding_client,
    get_rerank_client,
)

logger = get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "hackathon_requests_total",
    "Total requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "hackathon_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)
TOKENS_GENERATED = Counter(
    "hackathon_tokens_generated_total",
    "Total tokens generated",
    ["model"],
)

# Global clients
chat_client: NIMChatClient | MockNIMClient
embedding_client: NIMEmbeddingClient | MockNIMClient
rerank_client: NIMRerankClient | MockNIMClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager."""
    global chat_client, embedding_client, rerank_client

    # Startup
    configure_logging()
    settings = get_settings()

    logger.info(
        "application_starting",
        environment=settings.app.environment,
        mock_nim=settings.mock_nim,
    )

    chat_client = get_chat_client()
    embedding_client = get_embedding_client()
    rerank_client = get_rerank_client()

    # Health checks
    chat_healthy = await chat_client.health_check()
    embed_healthy = await embedding_client.health_check()
    rerank_healthy = await rerank_client.health_check()

    logger.info(
        "health_checks_complete",
        chat=chat_healthy,
        embedding=embed_healthy,
        rerank=rerank_healthy,
    )

    yield

    # Shutdown
    logger.info("application_shutting_down")
    await chat_client.close()
    await embedding_client.close()
    await rerank_client.close()


app = FastAPI(
    title="Nebius x NVIDIA Hackathon API",
    description="High-performance AI inference API for the Global AI Hackathon 2026",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency for API key auth
async def verify_api_key(
    x_api_key: Annotated[str | None, Header()] = None,
) -> None:
    settings = get_app_settings()
    if settings.api_key_enabled:
        if not x_api_key or x_api_key != settings.api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
            )


# Request/Response Models
class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str = "0.1.0"
    services: dict[str, bool]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=32000)
    session_id: str | None = None
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, ge=1, le=32768)
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
    session_id: str
    model: str
    usage: dict[str, int] | None = None
    latency_ms: float


class EmbedRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1, max_length=100)
    model: str | None = None


class RerankReq(BaseModel):
    query: str = Field(..., min_length=1)
    documents: list[str] = Field(..., min_length=1, max_length=50)
    top_n: int | None = Field(None, ge=1, le=50)


# Middleware for metrics
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    latency = time.perf_counter() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(latency)

    return response


# Routes
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        services={
            "chat": await chat_client.health_check(),
            "embedding": await embedding_client.health_check(),
            "rerank": await rerank_client.health_check(),
        },
    )


@app.get("/metrics", tags=["Monitoring"])
async def metrics() -> StreamingResponse:
    """Prometheus metrics endpoint."""
    return StreamingResponse(
        iter([generate_latest()]),
        media_type="text/plain",
    )


@app.post(
    "/api/v1/chat",
    response_model=ChatResponse,
    tags=["Chat"],
    dependencies=[Depends(verify_api_key)],
)
async def chat_completion(request: ChatRequest) -> ChatResponse:
    """Generate a chat completion."""
    start_time = time.perf_counter()
    session_id = request.session_id or str(uuid.uuid4())

    messages = [ChatMessage(role="user", content=request.message)]

    try:
        response = await chat_client.chat_completion(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            stream=False,
        )

        latency_ms = (time.perf_counter() - start_time) * 1000

        # Track tokens
        if response.usage:
            TOKENS_GENERATED.labels(model=response.model).inc(
                response.usage.get("completion_tokens", 0)
            )

        return ChatResponse(
            response=response.choices[0].message.content,
            session_id=session_id,
            model=response.model,
            usage=response.usage,
            latency_ms=latency_ms,
        )

    except Exception as e:
        logger.error("chat_endpoint_error", error=str(e), session_id=session_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat completion failed: {str(e)}",
        )


@app.post(
    "/api/v1/chat/stream",
    tags=["Chat"],
    dependencies=[Depends(verify_api_key)],
)
async def chat_completion_stream(request: ChatRequest):
    """Stream chat completion tokens."""
    session_id = request.session_id or str(uuid.uuid4())
    messages = [ChatMessage(role="user", content=request.message)]

    async def generate():
        try:
            async for chunk in chat_client.chat_completion_stream(
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
            ):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error("stream_error", error=str(e), session_id=session_id)
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@app.post(
    "/api/v1/embeddings",
    response_model=EmbeddingResponse,
    tags=["Embeddings"],
    dependencies=[Depends(verify_api_key)],
)
async def create_embeddings(request: EmbedRequest) -> EmbeddingResponse:
    """Create embeddings for texts."""
    try:
        return await embedding_client.embed(texts=request.texts)
    except Exception as e:
        logger.error("embedding_endpoint_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embedding failed: {str(e)}",
        )


@app.post(
    "/api/v1/rerank",
    response_model=RerankResponse,
    tags=["Rerank"],
    dependencies=[Depends(verify_api_key)],
)
async def rerank_documents(request: RerankReq) -> RerankResponse:
    """Rerank documents by relevance to query."""
    try:
        return await rerank_client.rerank(
            query=request.query,
            documents=request.documents,
            top_n=request.top_n,
        )
    except Exception as e:
        logger.error("rerank_endpoint_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rerank failed: {str(e)}",
        )


@app.get("/api/v1/models", tags=["Models"])
async def list_models():
    """List available models."""
    settings = get_nvidia_settings()
    return {
        "chat": settings.llm_model,
        "embedding": settings.embedding_model,
        "rerank": settings.rerank_model,
    }


if __name__ == "__main__":
    import uvicorn

    settings = get_app_settings()
    uvicorn.run(
        "src.api.routes:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        log_level=settings.log_level.lower(),
        reload=settings.environment == "development",
    )