"""NVIDIA NIM client wrapper for LLM and embedding inference."""

import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Optional

import httpx
from pydantic import BaseModel, Field

from src.core.config import get_nvidia_settings, get_settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class ChatMessage(BaseModel):
    """Chat message format."""

    role: str = Field(..., description="Message role: system, user, assistant")
    content: str = Field(..., description="Message content")


class ChatCompletionRequest(BaseModel):
    """Chat completion request."""

    model: str
    messages: list[ChatMessage]
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=1, le=32768)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    stream: bool = Field(default=False)
    stop: Optional[list[str]] = None


class ChatCompletionChoice(BaseModel):
    """Chat completion choice."""

    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class ChatCompletionResponse(BaseModel):
    """Chat completion response."""

    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[ChatCompletionChoice]
    usage: Optional[dict[str, int]] = None


class EmbeddingRequest(BaseModel):
    """Embedding request."""

    model: str
    input: list[str] | str
    encoding_format: str = "float"


class EmbeddingData(BaseModel):
    """Embedding data."""

    object: str = "embedding"
    index: int
    embedding: list[float]


class EmbeddingResponse(BaseModel):
    """Embedding response."""

    object: str = "list"
    data: list[EmbeddingData]
    model: str
    usage: dict[str, int]


class RerankRequest(BaseModel):
    """Rerank request."""

    model: str
    query: str
    documents: list[str]
    top_n: Optional[int] = None


class RerankResult(BaseModel):
    """Rerank result."""

    index: int
    relevance_score: float
    document: str


class RerankResponse(BaseModel):
    """Rerank response."""

    id: str
    model: str
    results: list[RerankResult]
    usage: dict[str, int]


@dataclass
class InferenceMetrics:
    """Metrics for inference calls."""

    latency_ms: float
    tokens_generated: int = 0
    tokens_per_second: float = 0.0
    success: bool = True
    error: Optional[str] = None


class BaseNIMClient(ABC):
    """Abstract base class for NIM clients."""

    def __init__(
        self,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        api_key: Optional[str] = None,
        timeout: float = 300.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or get_nvidia_settings().api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self.timeout,
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the service is healthy."""
        pass


class NIMChatClient(BaseNIMClient):
    """Client for NIM chat completions."""

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        api_key: Optional[str] = None,
        timeout: float = 300.0,
    ):
        super().__init__(base_url, api_key, timeout)
        self.model = model or get_nvidia_settings().llm_model

    async def health_check(self) -> bool:
        try:
            client = await self._get_client()
            response = await client.get("/models")
            return response.status_code == 200
        except Exception as e:
            logger.error("health_check_failed", error=str(e))
            return False

    async def chat_completion(
        self,
        messages: list[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs,
    ) -> ChatCompletionResponse:
        """Generate chat completion."""
        settings = get_nvidia_settings()

        request = ChatCompletionRequest(
            model=self.model,
            messages=messages,
            temperature=temperature or settings.tensorrt_max_batch_size and 0.7 or 0.7,
            max_tokens=max_tokens or settings.tensorrt_max_output_len,
            stream=stream,
            **kwargs,
        )

        start_time = time.perf_counter()
        metrics = InferenceMetrics(latency_ms=0)

        try:
            client = await self._get_client()
            response = await client.post(
                "/chat/completions",
                json=request.model_dump(exclude_none=True),
            )
            response.raise_for_status()

            metrics.latency_ms = (time.perf_counter() - start_time) * 1000
            metrics.success = True

            data = response.json()
            if "usage" in data:
                metrics.tokens_generated = data["usage"].get("completion_tokens", 0)
                if metrics.latency_ms > 0:
                    metrics.tokens_per_second = metrics.tokens_generated / (metrics.latency_ms / 1000)

            logger.info(
                "chat_completion_success",
                model=self.model,
                latency_ms=metrics.latency_ms,
                tokens_per_second=metrics.tokens_per_second,
            )

            return ChatCompletionResponse(**data)

        except Exception as e:
            metrics.latency_ms = (time.perf_counter() - start_time) * 1000
            metrics.success = False
            metrics.error = str(e)
            logger.error("chat_completion_failed", model=self.model, error=str(e))
            raise

    async def chat_completion_stream(
        self,
        messages: list[ChatMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> AsyncGenerator[str, None]:
        """Stream chat completion tokens."""
        settings = get_nvidia_settings()

        request = ChatCompletionRequest(
            model=self.model,
            messages=messages,
            temperature=temperature or 0.7,
            max_tokens=max_tokens or settings.tensorrt_max_output_len,
            stream=True,
            **kwargs,
        )

        client = await self._get_client()
        async with client.stream(
            "POST",
            "/chat/completions",
            json=request.model_dump(exclude_none=True),
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    yield data


class NIMEmbeddingClient(BaseNIMClient):
    """Client for NIM embeddings."""

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        api_key: Optional[str] = None,
        timeout: float = 60.0,
    ):
        super().__init__(base_url, api_key, timeout)
        self.model = model or get_nvidia_settings().embedding_model

    async def health_check(self) -> bool:
        try:
            client = await self._get_client()
            response = await client.get("/models")
            return response.status_code == 200
        except Exception as e:
            logger.error("embedding_health_check_failed", error=str(e))
            return False

    async def embed(
        self,
        texts: list[str],
        encoding_format: str = "float",
    ) -> EmbeddingResponse:
        """Generate embeddings for texts."""
        request = EmbeddingRequest(
            model=self.model,
            input=texts,
            encoding_format=encoding_format,
        )

        start_time = time.perf_counter()

        try:
            client = await self._get_client()
            response = await client.post(
                "/embeddings",
                json=request.model_dump(),
            )
            response.raise_for_status()

            latency_ms = (time.perf_counter() - start_time) * 1000
            logger.info("embedding_success", model=self.model, count=len(texts), latency_ms=latency_ms)

            return EmbeddingResponse(**response.json())

        except Exception as e:
            logger.error("embedding_failed", model=self.model, error=str(e))
            raise

    async def embed_single(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        response = await self.embed([text])
        return response.data[0].embedding


class NIMRerankClient(BaseNIMClient):
    """Client for NIM reranking."""

    def __init__(
        self,
        model: Optional[str] = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        api_key: Optional[str] = None,
        timeout: float = 60.0,
    ):
        super().__init__(base_url, api_key, timeout)
        self.model = model or get_nvidia_settings().rerank_model

    async def health_check(self) -> bool:
        try:
            client = await self._get_client()
            response = await client.get("/models")
            return response.status_code == 200
        except Exception as e:
            logger.error("rerank_health_check_failed", error=str(e))
            return False

    async def rerank(
        self,
        query: str,
        documents: list[str],
        top_n: Optional[int] = None,
    ) -> RerankResponse:
        """Rerank documents by relevance to query."""
        request = RerankRequest(
            model=self.model,
            query=query,
            documents=documents,
            top_n=top_n,
        )

        start_time = time.perf_counter()

        try:
            client = await self._get_client()
            response = await client.post(
                "/rerank",
                json=request.model_dump(exclude_none=True),
            )
            response.raise_for_status()

            latency_ms = (time.perf_counter() - start_time) * 1000
            logger.info("rerank_success", model=self.model, count=len(documents), latency_ms=latency_ms)

            return RerankResponse(**response.json())

        except Exception as e:
            logger.error("rerank_failed", model=self.model, error=str(e))
            raise


class MockNIMClient:
    """Mock NIM client for development without GPU/API access."""

    def __init__(self, *args, **kwargs):
        self.model = kwargs.get("model", "mock-model")

    async def health_check(self) -> bool:
        return True

    async def chat_completion(self, messages, **kwargs) -> ChatCompletionResponse:
        await asyncio.sleep(0.1)  # Simulate latency
        return ChatCompletionResponse(
            id="mock-completion",
            created=int(time.time()),
            model=self.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(role="assistant", content="This is a mock response."),
                    finish_reason="stop",
                )
            ],
            usage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        )

    async def chat_completion_stream(self, messages, **kwargs):
        yield '{"choices": [{"delta": {"content": "Mock "}}]}'
        await asyncio.sleep(0.05)
        yield '{"choices": [{"delta": {"content": "streaming "}}]}'
        await asyncio.sleep(0.05)
        yield '{"choices": [{"delta": {"content": "response."}}]}'
        yield "[DONE]"

    async def embed(self, texts, **kwargs) -> EmbeddingResponse:
        await asyncio.sleep(0.05)
        dim = 1024
        return EmbeddingResponse(
            object="list",
            data=[
                EmbeddingData(index=i, embedding=[0.1] * dim)
                for i in range(len(texts) if isinstance(texts, list) else 1)
            ],
            model=self.model,
            usage={"prompt_tokens": 10, "total_tokens": 10},
        )

    async def embed_single(self, text: str) -> list[float]:
        return [0.1] * 1024

    async def rerank(self, query: str, documents: list[str], **kwargs) -> RerankResponse:
        await asyncio.sleep(0.05)
        return RerankResponse(
            id="mock-rerank",
            model=self.model,
            results=[
                RerankResult(index=i, relevance_score=1.0 - i * 0.1, document=doc)
                for i, doc in enumerate(documents)
            ],
            usage={"total_tokens": 10},
        )

    async def close(self):
        pass


def get_chat_client() -> NIMChatClient | MockNIMClient:
    """Factory function to get appropriate chat client."""
    settings = get_settings()
    if settings.mock_nim:
        logger.info("using_mock_nim_client")
        return MockNIMClient()
    return NIMChatClient()


def get_embedding_client() -> NIMEmbeddingClient | MockNIMClient:
    """Factory function to get appropriate embedding client."""
    settings = get_settings()
    if settings.mock_nim:
        return MockNIMClient()
    return NIMEmbeddingClient()


def get_rerank_client() -> NIMRerankClient | MockNIMClient:
    """Factory function to get appropriate rerank client."""
    settings = get_settings()
    if settings.mock_nim:
        return MockNIMClient()
    return NIMRerankClient()