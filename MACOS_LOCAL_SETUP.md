# OllamaHub - macOS Local Setup Guide
**MacBook Pro i9 · 32GB RAM · M-Series/Intel GPU**

---

## 🎯 Quick Start (5 minutes)

### One-Time Setup
```bash
./scripts/setup-macos.sh
# Takes 5-15 min (mostly downloading model)
```

### Start Services
```bash
# Option 1: All at once (recommended)
./scripts/start-all.sh

# Option 2: Manual (3 terminals)
# Terminal 1
ollama serve

# Terminal 2
cd backend && source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000

# Terminal 3
cd frontend && npm run dev
```

### Access
- **App:** http://localhost:5173
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 📋 What Gets Installed

| Component | Version | Role |
|-----------|---------|------|
| **Ollama** | Latest | Local LLM runtime |
| **Model** | qwen:7b-coder | Primary code model (6GB) |
| **Python** | 3.11+ | Backend runtime |
| **FastAPI** | Latest | Backend API |
| **Node.js** | 20+ | Frontend build |
| **React** | 18+ | Frontend UI |

---

## 🔧 Configuration

**File:** `.env` (created from `.env.example`)

```env
# Model Configuration
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=mistral:latest
OLLAMA_TIMEOUT=300

# Backend
HOST=127.0.0.1
PORT=8000
DEBUG=True
ENVIRONMENT=development

# Frontend
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional Claude Integration
CLAUDE_API_KEY=sk-ant-...  # Leave empty if local-only
```

---

## 📊 Hardware Configuration

**Your System:**
- **CPU:** i9 (8+ cores)
- **RAM:** 32GB (good)
- **Model:** mistral:latest (4.4GB VRAM needed)
- **Latency:** ~30-50ms first token, then streaming

**Model Capabilities:**
- Excellent for general coding tasks
- 4.4GB size (lighter than alternatives)
- Very fast and responsive
- Supports: Python, JavaScript, TypeScript, Go, SQL, bash

---

## ✅ Verification Steps

1. **Check Ollama:**
   ```bash
   curl http://localhost:11434/api/tags
   ```
   Should see: `"name":"qwen:7b-coder"`

2. **Test Model:**
   ```bash
   ollama run qwen:7b-coder "Hello, what is 2+2?"
   ```

3. **Check Backend:**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status":"ok"}`

4. **Check Frontend:**
   Open http://localhost:5173 in browser

---

## 🐛 Troubleshooting

### "Ollama not found"
```bash
# Install via Homebrew
brew install ollama
# Start in background
nohup ollama serve > /tmp/ollama.log 2>&1 &
```

### "Model download stuck"
```bash
# Check download progress
tail -f /tmp/ollama.log

# Or start in foreground to watch
ollama pull qwen:7b-coder
```

### "Port already in use"
```bash
# Find what's using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

### "Python venv activation fails"
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "npm install fails"
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### "Backend can't connect to Ollama"
- Make sure Ollama is running: `ollama serve`
- Check OLLAMA_HOST in .env matches where Ollama is running
- Default: `http://127.0.0.1:11434`

---

## 📁 Project Structure

```
ollama-hub/
├── scripts/
│   ├── setup-macos.sh        ← Run once to set everything up
│   ├── start-all.sh          ← Start complete stack
│   ├── check-setup.sh        ← Verify current status
│   ├── model-manager.sh      ← Manage Ollama models
│   └── dev.sh                ← Development utilities
│
├── backend/
│   ├── app/
│   │   ├── main.py          ← FastAPI entry point
│   │   ├── config.py        ← Settings from .env
│   │   ├── api/             ← API endpoints
│   │   ├── services/        ← Business logic
│   │   └── models/          ← Database schemas
│   ├── tests/               ← pytest suite (75 tests)
│   ├── requirements.txt
│   └── venv/                ← Python virtual environment
│
├── frontend/
│   ├── src/
│   │   ├── pages/          ← React pages (Dashboard, Chat, etc)
│   │   ├── components/     ← Reusable UI components
│   │   └── services/       ← API client
│   ├── package.json
│   └── node_modules/       ← npm dependencies
│
├── .env                     ← Local configuration
├── .env.example             ← Configuration template
├── docker-compose.yml       ← Container orchestration
└── MACOS_LOCAL_SETUP.md    ← This file
```

---

## 🚀 Development Workflow

### Adding a Feature

1. **Backend (FastAPI):**
   ```bash
   cd backend
   source venv/bin/activate
   
   # Edit app/api/endpoints.py or app/services/
   # Add tests in tests/
   
   # Run tests
   pytest tests/ -v
   
   # Type checking
   mypy app/
   ```

2. **Frontend (React):**
   ```bash
   cd frontend
   
   # Edit src/pages/ or src/components/
   npm run dev  # Watch mode
   npm run build  # Production build
   ```

3. **Restart services:**
   - Backend auto-reloads (--reload flag)
   - Frontend hot-reloads (Vite)

---

## 📝 Useful Commands

```bash
# Check system status
./scripts/check-setup.sh

# List available Ollama models
ollama list

# Download additional model
ollama pull mistral:latest

# View Ollama logs (if running in background)
tail -f /tmp/ollama.log

# Backend tests
cd backend && pytest tests/ -v --cov=app

# Backend formatting
cd backend && black app/ && isort app/

# Frontend build
cd frontend && npm run build
```

---

## 🔐 Security Notes

- **Local Only:** No internet exposure (127.0.0.1)
- **Secrets:** Never commit .env file
- **API Key:** Optional (AUTH_ENABLED=False for local dev)
- **CORS:** Set to localhost only

For production deployment, see `NEXT_PHASE.md`

---

## 📚 Documentation

- **API:** See `/docs` endpoint when backend is running
- **Backend:** Check `backend/README.md`
- **Frontend:** Check `frontend/README.md`
- **Architecture:** See `SETUP.md`

---

## 💬 Tips

- **First run slow?** Model takes ~30s to load first time
- **Cache hits:** Identical prompts return instantly from cache
- **Use Claude:** For complex refactoring, use Claude (local is good for daily tasks)
- **Save projects:** Dashboard lets you save conversation history

---

## 🐚 Next Steps

1. Run setup: `./scripts/setup-macos.sh`
2. Verify: `./scripts/check-setup.sh`
3. Start: `./scripts/start-all.sh`
4. Open: http://localhost:5173
5. Try a code generation request in the chat

**Estimated total time:** 20 minutes (including model download)

---

**Last Updated:** June 29, 2026  
**Status:** Production Ready  
**Support:** Check backend logs: `tail -f /tmp/ollama.log`
