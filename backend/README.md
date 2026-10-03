# Master DSA - Backend

## 🚀 Overview

This is the backend for Master DSA - a platform to track your daily DSA practice with Python and C++.

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLModel** - ORM
- **Gemini AI** - Code analysis

## 📁 Project Structure
backend/
├── app/
│ ├── api/ # API endpoints
│ ├── core/ # Config, security
│ ├── models/ # Database models
│ ├── schemas/ # Pydantic schemas
│ ├── services/ # Business logic
│ └── utils/ # Utilities
├── tests/ # Test files
└── scripts/ # Utility scripts


## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd master-dsa-backend

2. Create virtual environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
bash
pip install -r requirements.txt
4. Set up environment variables
bash
cp .env.example .env
# Edit .env with your API keys
5. Start PostgreSQL
bash
docker-compose up -d
6. Initialize database
bash
python scripts/init_db.py
python scripts/seed_data.py
7. Run the server
bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
📚 API Documentation
Once running, visit:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

🔑 Environment Variables
Variable	Description
DATABASE_URL	PostgreSQL connection string
GEMINI_API_KEY	Google Gemini API key
ADMIN_USERNAME	Admin username for verification
CORS_ORIGINS	Allowed frontend origins
DEBUG	Enable debug mode