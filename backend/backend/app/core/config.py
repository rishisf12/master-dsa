import os
from typing import List
from dotenv import load_dotenv
from pathlib import Path

# Force load .env from the correct location
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / '.env'
load_dotenv(env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # App
    APP_NAME: str = os.getenv("APP_NAME", "Master DSA API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:9664914606v%40V@db.cilwiqskgmvmhyhnryfz.supabase.co:5432/postgres"
    )

    # AI - Gemini (legacy)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # AI - Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

    # Admin
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")

    # CORS
    CORS_ORIGINS: List[str] = [
        origin.strip() 
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:5173"
        ).split(",")
        if origin.strip()
    ]

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")


settings = Settings()

# Debug output
print(f"✅ DATABASE_URL: {settings.DATABASE_URL}")
print(f"✅ CORS_ORIGINS: {settings.CORS_ORIGINS}")
if settings.GROQ_API_KEY:
    print(f"✅ GROQ_API_KEY loaded: {settings.GROQ_API_KEY[:10]}...")
