# Master DSA - Monorepo

This repository combines the frontend and backend for the Master DSA project.

## Structure

```
master-dsa/
├── frontend/          # React + Vite frontend
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── backend/           # Python (FastAPI) backend
│   ├── api/
│   ├── backend/
│   ├── pyproject.toml
│   └── requirements.txt
│
└── README.md          # This file
```

## Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
# Using uv (recommended)
uv sync
uv run uvicorn backend.main:app --reload

# Or using pip
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

## Development

Run both services concurrently:

```bash
# Terminal 1 - Backend
cd backend && uv run uvicorn backend.main:app --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## Environment Variables

- **Frontend**: Copy `frontend/.env.production` to `frontend/.env` and adjust as needed
- **Backend**: Create `backend/.env` based on your configuration needs

## Original Repositories

- Frontend: https://github.com/rishisf12/master-dsa-frontend
- Backend: https://github.com/rishisf12/master-dsa-backend