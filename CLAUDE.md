# OllamaHub - Development Guide

## Overview

**Professional IDE for Local LLMs + Claude Integration**

- **Purpose:** Web UI for code work with Ollama (local) + optional Claude (cloud)
- **Status:** Production-Ready on master, setup/macos-local-model branch for this MacBook
- **Tech:** React 18 + FastAPI + SQLite + Ollama
- **Model:** qwen:7b-coder (6GB VRAM, 67.3% HumanEval)

## Quick Start

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2 & 3: Start backend + frontend
./scripts/start-all.sh
```

Access: http://localhost:5173

## Setup (One Time)

```bash
./scripts/setup-macos.sh
# Takes 5-15 minutes (mostly downloading model)
```

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── config.py         # Settings from .env
│   ├── api/
│   │   ├── chat.py       # Chat endpoints
│   │   ├── status.py     # Status/health
│   │   ├── projects.py   # Project management
│   │   └── models.py     # Model endpoints
│   ├── services/         # Business logic
│   └── models/           # SQLite schemas
├── tests/                # 75 pytest tests
├── requirements.txt
└── venv/

frontend/
├── src/
│   ├── pages/           # Dashboard, Chat, Admin
│   ├── components/      # UI components
│   ├── services/        # API client
│   └── App.tsx          # Main app
├── package.json
└── node_modules/
```

## Configuration

**File:** `.env` (auto-created from `.env.example`)

Key variables:
- `OLLAMA_MODEL=qwen:7b-coder` — Code model for this setup
- `OLLAMA_HOST=http://127.0.0.1:11434` — Local Ollama
- `PORT=8000` — Backend API port
- `CLAUDE_API_KEY=sk-ant-...` — Optional, leave empty for local-only

## Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | System health |
| POST | `/api/chat` | Send message, get response (streaming) |
| GET | `/api/models` | List available Ollama models |
| POST | `/api/projects` | Save project/conversation |
| GET | `/api/status` | Ollama + Claude availability |

Full docs at `/docs` when backend running.

## Development Tasks

### Backend

```bash
cd backend
source venv/bin/activate

# Run in debug mode
python -m uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Type checking
mypy app/

# Format code
black app/
isort app/
```

### Frontend

```bash
cd frontend

# Dev server (hot reload)
npm run dev

# Build for production
npm run build

# Type checking
npx tsc --noEmit
```

## Testing

**Backend:** 75 pytest tests
```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov=app
```

**Frontend:** React Testing Library (optional)

## Debugging

### Backend not connecting to Ollama?
1. Verify Ollama running: `curl http://localhost:11434/api/tags`
2. Check OLLAMA_HOST in .env
3. Check Ollama logs: `tail -f /tmp/ollama.log`

### Model taking too long?
- First load: ~30s to load model into VRAM
- Subsequent: <100ms TTFT (first token time)
- Check available VRAM: `ollama ps`

### Frontend not updating?
- Make sure npm run dev is in watch mode
- Vite should auto-reload on file changes
- Check browser console for errors

## Git Workflow

**Branches:**
- `master` — Production-ready code
- `setup/macos-local-model` — This MacBook's local setup
- Feature branches as needed

**For this setup branch:**
- Changes to setup scripts
- Local configuration documentation
- Hardware-specific optimizations

## When to Use Claude vs Local

| Task | Use |
|------|-----|
| Daily coding, prototyping | Local (Qwen 7B) |
| Complex architecture | Claude |
| Code review, critical features | Claude |
| Refactoring, boilerplate | Local |
| Testing setup locally first | Local |

Local is 93% cheaper and good for daily work.

## Important Files

- `.env` — **Never commit** (secrets inside)
- `backend/requirements.txt` — Backend dependencies
- `frontend/package.json` — Frontend dependencies
- `MACOS_LOCAL_SETUP.md` — Setup guide for this hardware
- `QUICKSTART.md` — General quick start
- `docker-compose.yml` — Container orchestration (optional)

## Performance Baseline (This Setup)

- **Model:** Qwen 7B Coder
- **VRAM:** ~6GB (fits on i9)
- **Latency:** 50-100ms TTFT, then streaming
- **Context:** 128K tokens (2-3 files)
- **Quality:** 67.3% HumanEval (good for daily tasks)

## Commands Summary

```bash
# Setup (once)
./scripts/setup-macos.sh

# Daily
./scripts/start-all.sh

# Verify status
./scripts/check-setup.sh

# Manage models
./scripts/model-manager.sh

# Backend
cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev

# Tests
cd backend && pytest tests/ -v
```

## Known Limitations

- **VRAM:** Limited to ~6GB with Qwen 7B
- **Quality:** Use Claude for critical code reviews
- **Context:** Max ~128K tokens effective per request
- **No persistence:** Projects saved to SQLite, not cloud

## Next Phase Features

- [ ] Prometheus metrics
- [ ] Redis caching
- [ ] Docker deployment
- [ ] Multi-user support
- [ ] Conversation history export
- [ ] Custom model fine-tuning

## Support

- **API Docs:** `/docs` endpoint
- **Backend Logs:** Terminal where you ran backend
- **Ollama Logs:** `/tmp/ollama.log`
- **Frontend Console:** Browser developer tools
- **Tests:** `pytest tests/ -v` for diagnostics

## Notes

- This is a sub-branch (setup/macos-local-model) for local configuration
- Keep master branch clean (production-ready)
- Scripts are Mac-specific (Homebrew, etc)
- For Linux/Windows, modify scripts accordingly

---

**Status:** Ready for local development  
**Last Updated:** June 29, 2026
