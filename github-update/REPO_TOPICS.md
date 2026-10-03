# GitHub Repository Topics for Hackathon

Run these commands to add hackathon-relevant topics to your existing repositories.

## Topics to Add

### Master DSA Backend (`master-dsa-backend`)
```bash
gh repo edit rishisf12/master-dsa-backend --add-topic python,dsa,algorithms,data-structures,fastapi,backend,nvidia,ai,hackathon,nebius
```

### Master DSA Frontend (`master-dsa-frontend`)
```bash
gh repo edit rishisf12/master-dsa-frontend --add-topic javascript,react,dsa,algorithms,visualization,frontend,nvidia,ai,hackathon,nebius
```

### CampusPilot (`CampusPilot`)
```bash
gh repo edit rishisf12/CampusPilot --add-topic python,campus,college,platform,nvidia,ai,hackathon,nebius
```

### Portfolio Website (`Portfolio-Website`)
```bash
gh repo edit rishisf12/Portfolio-Website --add-topic javascript,react,portfolio,personal-website,nvidia,ai,hackathon,nebius
```

### UrTeam (`UrTeam`)
```bash
gh repo edit rishisf12/UrTeam --add-topic javascript,campus,collaboration,team,nvidia,ai,hackathon,nebius
```

### PocketF (`pocketF`)
```bash
gh repo edit rishisf12/pocketF --add-topic python,expense-tracker,finance,personal-finance,nvidia,ai,hackathon,nebius
```

## Create Profile README Repository

Create a special repository named `rishisf12` (same as username) for your profile README:

```bash
# Create the repo on GitHub first (via web or CLI)
gh repo create rishisf12 --public --description "🚀 Rishi's GitHub Profile - AI/ML Engineer | Nebius x NVIDIA Hackathon 2026 Participant"

# Then push the profile README
cd github-update/profile-readme
git init
git add README.md
git commit -m "Add profile README with hackathon info"
git branch -M main
git remote add origin https://github.com/rishisf12/rishisf12.git
git push -u origin main
```

## Create Hackathon Showcase Repository

```bash
# Create the repo
gh repo create rishisf12/nebius-nvidia-hackathon-showcase --public --description "🏆 Nebius x NVIDIA Global AI Hackathon 2026 Submission - High-performance AI with NIM, NeMo, Triton & TensorRT-LLM"

# Push the showcase repo
cd github-update/nebius-nvidia-hackathon-showcase
git init
git add .
git commit -m "Initial hackathon submission structure"
git branch -M main
git remote add origin https://github.com/rishisf12/nebius-nvidia-hackathon-showcase.git
git push -u origin main
```

## Quick Setup Script

Save as `setup-hackathon-repos.sh` and run:

```bash
#!/bin/bash
# setup-hackathon-repos.sh

# Add topics to existing repos
gh repo edit rishisf12/master-dsa-backend --add-topic "python,dsa,algorithms,data-structures,fastapi,backend,nvidia,ai,hackathon,nebius"
gh repo edit rishisf12/master-dsa-frontend --add-topic "javascript,react,dsa,algorithms,visualization,frontend,nvidia,ai,hackathon,nebius"
gh repo edit rishisf12/CampusPilot --add-topic "python,campus,college,platform,nvidia,ai,hackathon,nebius"
gh repo edit rishisf12/Portfolio-Website --add-topic "javascript,react,portfolio,personal-website,nvidia,ai,hackathon,nebius"
gh repo edit rishisf12/UrTeam --add-topic "javascript,campus,collaboration,team,nvidia,ai,hackathon,nebius"
gh repo edit rishisf12/pocketF --add-topic "python,expense-tracker,finance,personal-finance,nvidia,ai,hackathon,nebius"

echo "✅ Topics added to all existing repositories"
echo ""
echo "Next steps:"
echo "1. Create profile README repo: gh repo create rishisf12 --public"
echo "2. Create hackathon showcase repo: gh repo create rishisf12/nebius-nvidia-hackathon-showcase --public"
echo "3. Push the generated files from github-update/ directory"
```

## Verify Topics Added

```bash
# Check topics for a repo
gh repo view rishisf12/master-dsa-backend --json topics

# List all repos with topics
gh repo list rishisf12 --json name,topics --jq '.[] | "\(.name): \(.topics | join(", "))"'
```

## Recommended Additional Topics

Consider adding these to relevant repos:

| Topic | Use For |
|-------|---------|
| `nvidia-nim` | Repos using NVIDIA NIM microservices |
| `tensorrt-llm` | Repos with TensorRT-LLM optimization |
| `nemo-retriever` | Repos using NeMo Retriever |
| `nemo-guardrails` | Repos with NeMo Guardrails |
| `triton-inference` | Repos deploying with Triton |
| `nebius-cloud` | Repos deployed on Nebius AI Cloud |
| `llm-optimization` | LLM performance optimization |
| `rag` | Retrieval-Augmented Generation |
| `ai-agents` | Autonomous AI agents |
| `hackathon-2026` | Hackathon-specific tag |