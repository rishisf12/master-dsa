"""Core configuration management for the hackathon project."""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class NVIDIASettings(BaseSettings):
    """NVIDIA-specific configuration."""

    api_key: str = Field(..., description="NVIDIA API key from build.nvidia.com")
    org: Optional[str] = Field(None, description="NVIDIA organization name")

    # NIM Models
    llm_model: str = Field(default="meta/llama3-70b-instruct", description="NIM LLM model")
    embedding_model: str = Field(
        default="nvidia/nv-embedqa-e5-v5", description="NIM embedding model"
    )
    rerank_model: str = Field(
        default="nvidia/nv-rerankqa-mistral-4b-v3", description="NIM rerank model"
    )

    # TensorRT-LLM
    tensorrt_enabled: bool = Field(default=True, description="Enable TensorRT-LLM optimization")
    tensorrt_quantization: Literal["fp8", "int4", "awq", "none"] = Field(
        default="fp8", description="Quantization mode"
    )
    tensorrt_max_batch_size: int = Field(default=32, ge=1, le=128)
    tensorrt_max_input_len: int = Field(default=4096, ge=512, le=32768)
    tensorrt_max_output_len: int = Field(default=2048, ge=512, le=32768)

    model_config = SettingsConfigDict(env_prefix="NVIDIA_", extra="ignore")


class NebiusSettings(BaseSettings):
    """Nebius AI Cloud configuration."""

    api_key: str = Field(..., description="Nebius API key")
    project_id: str = Field(..., description="Nebius project ID")
    cluster_id: str = Field(..., description="Nebius cluster ID")
    region: str = Field(default="us-east-1", description="Nebius region")

    gpu_type: Literal["h100", "a100", "l40s"] = Field(default="h100")
    gpu_count: int = Field(default=1, ge=1, le=8)

    model_config = SettingsConfigDict(env_prefix="NEBIUS_", extra="ignore")


class VectorDBSettings(BaseSettings):
    """Vector database (Qdrant) configuration."""

    url: str = Field(default="http://localhost:6333")
    api_key: Optional[str] = Field(default=None)
    collection_name: str = Field(default="hackathon_knowledge_base")
    vector_size: int = Field(default=1024, description="Embedding dimension")
    distance: Literal["Cosine", "Euclid", "Dot"] = Field(default="Cosine")

    model_config = SettingsConfigDict(env_prefix="QDRANT_", extra="ignore")


class RedisSettings(BaseSettings):
    """Redis configuration."""

    url: str = Field(default="redis://localhost:6379")
    password: Optional[str] = Field(default=None)
    db: int = Field(default=0, ge=0, le=15)

    model_config = SettingsConfigDict(env_prefix="REDIS_", extra="ignore")


class TritonSettings(BaseSettings):
    """Triton Inference Server configuration."""

    url: str = Field(default="http://localhost:8000")
    grpc_url: str = Field(default="localhost:8001")
    model_repository: str = Field(default="./docker/triton/model_repository")

    model_config = SettingsConfigDict(env_prefix="TRITON_", extra="ignore")


class AppSettings(BaseSettings):
    """Main application settings."""

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000, ge=1, le=65535)
    workers: int = Field(default=1, ge=1, le=32)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(default="INFO")
    environment: Literal["development", "staging", "production"] = Field(default="development")

    # Security
    api_key_enabled: bool = Field(default=False)
    api_key: Optional[str] = Field(default=None)
    jwt_secret_key: str = Field(..., description="JWT signing secret")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_minutes: int = Field(default=60, ge=5, le=1440)

    # Rate limiting
    rate_limit_requests: int = Field(default=100, ge=1)
    rate_limit_window_seconds: int = Field(default=60, ge=1)

    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")


class ObservabilitySettings(BaseSettings):
    """Observability and monitoring settings."""

    # LangSmith
    langsmith_api_key: Optional[str] = Field(default=None)
    langsmith_project: str = Field(default="nebius-nvidia-hackathon")
    langsmith_endpoint: str = Field(default="https://api.smith.langchain.com")

    # Prometheus/Grafana
    prometheus_enabled: bool = Field(default=True)
    prometheus_port: int = Field(default=9090)
    grafana_enabled: bool = Field(default=True)
    grafana_port: int = Field(default=3000)

    metrics_prefix: str = Field(default="hackathon")

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")


class AgentSettings(BaseSettings):
    """Agent configuration."""

    max_iterations: int = Field(default=10, ge=1, le=50)
    timeout_seconds: int = Field(default=300, ge=30, le=3600)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4096, ge=256, le=32768)

    model_config = SettingsConfigDict(env_prefix="AGENT_", extra="ignore")


class RAGSettings(BaseSettings):
    """RAG pipeline configuration."""

    chunk_size: int = Field(default=512, ge=128, le=4096)
    chunk_overlap: int = Field(default=50, ge=0, le=512)
    top_k: int = Field(default=5, ge=1, le=50)
    similarity_threshold: float = Field(default=0.7, ge=0.0, le=1.0)
    rerank_top_k: int = Field(default=3, ge=1, le=20)

    model_config = SettingsConfigDict(env_prefix="RAG_", extra="ignore")


class GuardrailsSettings(BaseSettings):
    """NeMo Guardrails configuration."""

    enabled: bool = Field(default=True)
    config_path: str = Field(default="./config/guardrails")

    model_config = SettingsConfigDict(env_prefix="GUARDRAILS_", extra="ignore")


class Settings(BaseSettings):
    """Master settings aggregator."""

    nvidia: NVIDIASettings = Field(default_factory=NVIDIASettings)
    nebius: NebiusSettings = Field(default_factory=NebiusSettings)
    vector_db: VectorDBSettings = Field(default_factory=VectorDBSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    triton: TritonSettings = Field(default_factory=TritonSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    observability: ObservabilitySettings = Field(default_factory=ObservabilitySettings)
    agent: AgentSettings = Field(default_factory=AgentSettings)
    rag: RAGSettings = Field(default_factory=RAGSettings)
    guardrails: GuardrailsSettings = Field(default_factory=GuardrailsSettings)

    # Development
    debug_sql: bool = Field(default=False)
    mock_nim: bool = Field(default=False)
    mock_triton: bool = Field(default=False)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("nvidia", "nebius", "app", mode="before")
    @classmethod
    def validate_required_sections(cls, v):
        if isinstance(v, dict):
            return v
        return {}


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Convenience accessors
def get_nvidia_settings() -> NVIDIASettings:
    return get_settings().nvidia


def get_nebius_settings() -> NebiusSettings:
    return get_settings().nebius


def get_app_settings() -> AppSettings:
    return get_settings().app