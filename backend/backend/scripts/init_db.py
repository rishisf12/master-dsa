import sys
from pathlib import Path

# Add current directory (inner backend) to path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from sqlmodel import SQLModel
from app.db.session import engine
from app.models import base
from app.utils.logger import logger
from dotenv import load_dotenv

# ✅ Load .env file from the correct location
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)


def init_database():
    """Initialize the database by creating all tables."""
    try:
        logger.info("Creating database tables...")
        SQLModel.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Initializing Master DSA Database...")
    success = init_database()
    if success:
        print("✅ Database initialized successfully!")
    else:
        print("❌ Database initialization failed!")
        sys.exit(1)
