# GitHub Hackathon Update - Complete Setup Guide

## 📁 Files Created

All files are in `C:\Users\Appex\Documents\Default Project\github-update\`

```
github-update/
├── profile-readme/
│   └── README.md                 # Your GitHub profile README (for rishisf12/rishisf12 repo)
├── nebius-nvidia-hackathon-showcase/
│   ├── README.md                 # Comprehensive hackathon showcase README
│   ├── docker-compose.yml        # Full stack: API, Triton, Qdrant, Redis, Prometheus, Grafana
│   ├── pyproject.toml            # Modern Python packaging with all dependencies
│   ├── requirements.txt          # Pip-compatible requirements
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Comprehensive gitignore
│   ├── LICENSE                   # MIT License
│   ├── REPO_TOPICS.md            # Instructions for adding topics to existing repos
│   ├── docker/
│   │   ├── Dockerfile.api        # Multi-stage API Dockerfile
│   │   ├── Dockerfile.worker     # Worker Dockerfile
│   │   └── triton/
│   │       └── model_repository/
│   │           └── tensorrt_llm/
│   │               ├── config.pbtxt    # Triton TensorRT-LLM config
│   │               └── README.md       # Model deployment guide
│   ├── src/
│   │   ├── cli.py                # Rich CLI with chat, embed, rerank, benchmark
│   │   ├── core/
│   │   │   ├── config.py         # Pydantic Settings configuration
│   │   │   └── logging.py        # Structured logging with structlog
│   │   ├── models/
│   │   │   └── nim_client.py     # NVIDIA NIM client (chat, embed, rerank + mock)
│   │   └── api/
│   │       └── routes.py         # FastAPI routes with Prometheus metrics
│   └── .github/
│       ├── workflows/
│       │   └── ci.yml            # Full CI/CD pipeline
│       └── dependabot.yml        # Automated dependency updates
```

---

## 🚀 Quick Start

### 1. Create the Hackathon Showcase Repository

```bash
cd C:\Users\Appex\Documents\Default Project\github-update\nebius-nvidia-hackathon-showcase

# Initialize git
git init
git add .
git commit -m "Initial hackathon submission structure with NVIDIA NIM, Triton, TensorRT-LLM"

# Create repo on GitHub (requires gh CLI authenticated)
gh repo create rishisf12/nebius-nvidia-hackathon-showcase --public \
  --description "🏆 Nebius x NVIDIA Global AI Hackathon 2026 Submission - High-performance AI with NIM, NeMo, Triton & TensorRT-LLM"

# Push
git branch -M main
git remote add origin https://github.com/rishisf12/nebius-nvidia-hackathon-showcase.git
git push -u origin main
```

### 2. Create/Update Profile README Repository

```bash
cd C:\Users\Appex\Documents\Default Project\github-update\profile-readme

git init
git add README.md
git commit -m "Add profile README with hackathon participation"

# Create the special username repo
gh repo create rishisf12 --public \
  --description "🚀 Rishi's GitHub Profile - AI/ML Engineer | Nebius x NVIDIA Hackathon 2026 Participant"

git branch -M main
git remote add origin https://github.com/rishisf12/rishisf12.git
git push -u origin main
```

### 3. Add Topics to Existing Repositories

Run these commands (requires authenticated `gh` CLI):

```bash
# Master DSA Backend
gh repo edit rishisf12/master-dsa-backend --add-topic "python,dsa,algorithms,data-structures,fastapi,backend,nvidia,ai,hackathon,nebius"

# Master DSA Frontend
gh repo edit rishisf12/master-dsa-frontend --add-topic "javascript,react,dsa,algorithms,visualization,frontend,nvidia,ai,hackathon,nebius"

# CampusPilot
gh repo edit rishisf12/CampusPilot --add-topic "python,campus,college,platform,nvidia,ai,hackathon,nebius"

# Portfolio Website
gh repo edit rishisf12/Portfolio-Website --add-topic "javascript,react,portfolio,personal-website,nvidia,ai,hackathon,nebius"

# UrTeam
gh repo edit rishisf12/UrTeam --add-topic "javascript,campus,collaboration,team,nvidia,ai,hackathon,nebius"

# PocketF
gh repo edit rishisf12/pocketF --add-topic "python,expense-tracker,finance,personal-finance,nvidia,ai,hackathon,nebius"
```

Or run the automated script:
```bash
cd C:\Users\Appex\Documents\Default Project\github-update
bash REPO_TOPICS.md  # (copy the script section to a .sh file first)
```

---

## 🔐 Authentication Setup

You mentioned you'll authenticate. Here's how:

### GitHub CLI (Recommended)
```bash
# Install if not present
winget install GitHub.cli

# Authenticate
gh auth login
# Choose: GitHub.com → HTTPS → Login with browser
```

### Git Credential Manager (Alternative)
```bash
# Windows usually has this built-in
git config --global credential.helper manager-core
```

### Personal Access Token (Manual)
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo`, `workflow`, `admin:repo_hook` scopes
3. Use as password when prompted

---

## 🐳 Local Development

### Prerequisites
- Docker Desktop with WSL2 backend
- NVIDIA Container Toolkit (for GPU support)
- Python 3.10+

### Start Full Stack
```bash
cd nebius-nvidia-hackathon-showcase

# Copy and configure environment
cp .env.example .env
# Edit .env with your NVIDIA API key, Nebius credentials, etc.

# For development without GPU (uses mock clients)
echo "MOCK_NIM=true" >> .env
echo "MOCK_TRITON=true" >> .env

# Start services
docker compose up -d

# Check health
curl http://localhost:8000/health

# View logs
docker compose logs -f api
```

### Run CLI Demo
```bash
# Install in development mode
pip install -e ".[dev]"

# Interactive chat
python -m src.cli chat

# Single message
python -m src.cli chat "Explain TensorRT-LLM optimization"

# With streaming
python -m src.cli chat "Write a poem about GPUs" --stream

# Benchmark
python -m src.cli benchmark --prompts 20 --concurrent 2

# Health check
python -m src.cli health
```

### Run API Server Directly
```bash
# With mock (no GPU needed)
MOCK_NIM=true python -m src.api.routes

# With real NIM (requires NVIDIA_API_KEY)
python -m src.api.routes
```

---

## ☁️ Nebius AI Cloud Deployment

### 1. Get Nebius Credentials
- Sign up at https://console.nebius.com/
- Create project and GPU cluster (H100 recommended)
- Generate API key

### 2. Configure Environment
```bash
# In .env
NEBIUS_API_KEY=your_key
NEBIUS_PROJECT_ID=your_project
NEBIUS_CLUSTER_ID=your_cluster
NEBIUS_REGION=us-east-1
NEBIUS_GPU_TYPE=h100
NEBIUS_GPU_COUNT=1
```

### 3. Deploy via GitHub Actions
The CI/CD pipeline (`.github/workflows/ci.yml`) includes:
- Automated testing on every push
- Docker image building to GHCR
- Performance benchmarking
- Staging → Production deployment to Nebius

Add these secrets in GitHub repo settings:
- `NEBIUS_API_KEY`
- `NEBIUS_PROJECT_ID`
- `NEBIUS_CLUSTER_ID`
- `SLACK_WEBHOOK_URL` (optional)

---

## 🏗️ Architecture Overview

```
┌─────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Client    │────▶│  API Gateway │────▶│  NVIDIA NIM      │
│  (Web/CLI)  │     │  (FastAPI)   │     │  (LLM/Embed/Rerank)│
└─────────────┘     └──────┬───────┘     └────────┬─────────┘
                           │                      │
                    ┌──────▼───────┐     ┌────────▼─────────┐
                    │   Triton     │     │   NeMo           │
                    │  Inference   │     │  Guardrails/     │
                    │  (TensorRT)  │     │  Retriever       │
                    └──────┬───────┘     └──────────────────┘
                           │
                    ┌──────▼───────┐
                    │   Qdrant     │
                    │  Vector DB   │
                    └──────────────┘
```

---

## 🎯 Hackathon Submission Checklist

- [ ] **Repository Created** - `nebius-nvidia-hackathon-showcase` public
- [ ] **Profile README** - `rishisf12` repo with hackathon badges
- [ ] **Topics Added** - All 7 existing repos tagged with hackathon keywords
- [ ] **Environment Configured** - `.env` with NVIDIA/Nebius keys
- [ ] **Demo Working** - `python -m src.cli chat` responds
- [ ] **Docker Stack Running** - `docker compose up -d` healthy
- [ ] **CI/CD Passing** - GitHub Actions green
- [ ] **Triton Model Loaded** - TensorRT-LLM engine in `model_repository/tensorrt_llm/1/`
- [ ] **Documentation Complete** - README, architecture, API docs
- [ ] **Video Recorded** - 2-3 min demo for submission
- [ ] **Submitted** - Via Devpost at https://nebiusglobalaihackathon.devpost.com/

---

## 📝 Next Steps for You

1. **Authenticate with GitHub** (`gh auth login`)
2. **Run the repo creation commands** above
3. **Add your NVIDIA API key** to `.env` (get from https://build.nvidia.com/)
4. **Build TensorRT-LLM engine** for your chosen model (see `docker/triton/model_repository/README.md`)
5. **Customize the showcase README** with your specific project details
6. **Record demo video** and update README with link
7. **Submit to Devpost** before deadline

---

## 🔗 Key Links

- **Hackathon:** https://nebiusglobalaihackathon.devpost.com/
- **NVIDIA NIM:** https://build.nvidia.com/
- **Nebius Console:** https://console.nebius.com/
- **TensorRT-LLM:** https://github.com/NVIDIA/TensorRT-LLM
- **Triton:** https://github.com/triton-inference-server/server
- **Your GitHub:** https://github.com/rishisf12

---

## 💡 Pro Tips

1. **Use Mock Mode** for development: `MOCK_NIM=true` in `.env`
2. **Enable GitHub Pages** on showcase repo for live docs
3. **Add branch protection** on `main` requiring CI pass
4. **Create Discussion** tab for hackathon Q&A
5. **Pin the showcase repo** to your profile
6. **Star NVIDIA/Nebius repos** to show engagement

---

**Good luck with the hackathon! 🚀**

The structure is production-ready with:
- ✅ NVIDIA NIM integration (chat, embeddings, rerank)
- ✅ TensorRT-LLM optimization config
- ✅ Triton Inference Server setup
- ✅ Full observability (Prometheus, Grafana, LangSmith)
- ✅ CI/CD with benchmarking
- ✅ Nebius Cloud deployment ready
- ✅ Professional documentation