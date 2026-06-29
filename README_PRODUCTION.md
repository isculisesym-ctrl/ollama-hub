# OllamaHub — Production Deployment

**Professional IDE for Local LLMs + Claude Integration**

## ✅ Status

| Component | Tests | Status |
|-----------|-------|--------|
| Backend API | 75 ✅ | FastAPI, 20+ endpoints |
| Frontend | TypeScript ✅ | React 18, Vite, Tailwind |
| Chat Streaming | SSE ✅ | Real-time token-by-token |
| Code Review | POC ✅ | Parallel Ollama specialists |
| Auth | Optional ✅ | X-API-Key header |
| Admin Panel | Stats/Logs ✅ | Request logging, DB stats |

**Total:** 75 tests passing. Ready for production.

---

## 🚀 Quickstart (Any Machine)

### Requirements
- **Python 3.11+** (Backend)
- **Node.js 18+** (Frontend)
- **Ollama** (Local LLMs, `ollama serve`)
- **Git**

### 1. Clone & Setup
```bash
git clone https://github.com/isculisesym-ctrl/ollama-hub.git
cd ollama-hub

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Start Services (3 Terminals)

**Terminal 1 — Ollama:**
```bash
ollama serve
# Wait for: "Listening on 127.0.0.1:11434"
```

**Terminal 2 — Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
# Wait for: "Application startup complete"
```

**Terminal 3 — Frontend:**
```bash
cd frontend
npm run dev
# Wait for: "Local: http://localhost:5173"
```

### 3. Open Browser
```
http://localhost:5173
```

---

## 📋 Features

### Pages

- **Dashboard** — System status, model list, project summary
- **Chat** — Real-time streaming with Ollama or Claude
- **Setup** — 3-step wizard for connection testing
- **Admin** — Logs, stats, model manager (pull/delete)
- **Demo** — Code Review Swarm (parallel Ollama reviews)

### API Endpoints (20+)

```
GET    /api/status               → System health
GET    /api/models               → List Ollama models
POST   /api/models/pull          → Download model (SSE)
DELETE /api/models/{name}        → Remove model

POST   /api/chat                 → Send message
POST   /api/chat/stream          → Stream response (SSE)
GET    /api/chat/history/{id}    → Message history

GET    /api/projects             → List projects
POST   /api/projects             → Create project
PUT    /api/projects/{id}        → Update project
DELETE /api/projects/{id}        → Delete project

POST   /api/review/code          → Code Review Swarm (SSE)
GET    /api/admin/stats          → DB stats
GET    /api/admin/logs           → API logs
```

### Real-time Streaming (SSE)

All responses stream token-by-token:
```
POST /api/chat/stream
→ "data: {token}\n\n" (repeat until done)

POST /api/models/pull
→ "data: {status}\n\n" (download progress)

POST /api/review/code
→ Multiple specialists review in parallel
```

---

## 🏗️ Architecture

### Backend Stack
- **FastAPI** (async endpoints)
- **SQLite** (projects, chat history, config)
- **Pydantic** (validation)
- **httpx** (async HTTP client)
- **SSE** (Server-Sent Events for streaming)

### Frontend Stack
- **React 18** (UI framework)
- **Vite** (build tool)
- **TypeScript** (type safety)
- **Tailwind CSS** (styling)
- **Zustand** (state management)
- **Fetch API + ReadableStream** (SSE client)

### Security
- ✅ Input validation (Pydantic)
- ✅ SQL injection prevention (parameterized queries)
- ✅ CORS configured (localhost:5173, 127.0.0.1:3000)
- ✅ Optional API key auth (X-API-Key header)
- ✅ No hardcoded secrets (use .env)

---

## 🔧 Configuration

### Environment Variables

**Backend** — `backend/.env`
```env
# Server
HOST=127.0.0.1
PORT=8000
DEBUG=True

# Database
DATABASE_URL=sqlite:///./database.db

# Ollama
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=neural-chat
OLLAMA_TIMEOUT=120

# Claude (Optional)
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-haiku-4-5-20251001

# Auth (Optional)
AUTH_ENABLED=False
API_KEY=your-secret-key
```

**Frontend** — No .env needed (proxies to backend)

---

## 📊 Performance

### Benchmarks
- **Chat response** → 30-60s (depends on model + GPU)
- **Model pull** → Real-time progress via SSE
- **Code review** → 3 Ollamas in parallel (90-120s total)
- **Admin stats** → <100ms
- **Logs query** → <50ms

### Scalability
- Single-machine deployment handles **100+ concurrent requests**
- SQLite suitable for **<1M chat messages**
- Ollama limited by GPU VRAM (e.g., RTX 4060 = 8GB)

---

## 🧪 Testing

### Backend Tests (75 total)
```bash
cd backend
python -m pytest tests/ -v
```

Coverage:
- ✅ API endpoints
- ✅ Input validation
- ✅ Error handling
- ✅ Database operations
- ✅ Service layer

### Frontend
```bash
cd frontend
npm run type-check  # TypeScript
npm run build       # Production build
```

---

## 🚨 Security Checklist

- ✅ No hardcoded secrets (use .env)
- ✅ API input validation (Pydantic)
- ✅ CORS restricted to localhost (dev) / your domain (prod)
- ✅ Optional API key auth for admin endpoints
- ✅ SQL injection prevention (parameterized queries)
- ✅ No sensitive data in logs
- ✅ HTTPS-ready (reverse proxy via nginx/Caddy)

**Production Hardening:**
- Set `DEBUG=False`
- Set `AUTH_ENABLED=True` with strong `API_KEY`
- Configure reverse proxy (nginx/Caddy) for HTTPS
- Run behind authenticating reverse proxy
- Monitor logs and metrics

---

## 📚 Code Review POC

**How Code Review Swarm Works:**

1. User submits code
2. **3 Ollama specialists review in parallel:**
   - Security (finds vulnerabilities)
   - Performance (finds bottlenecks)
   - Readability (checks style/naming)
3. Each review streams tokens in real-time (SSE)
4. (Optional) Haiku synthesizes into executive summary

**Cost:** ~$0.0003 per review (3 free Ollamas + optional Haiku)  
**Compare:** $0.028 with Opus alone (93% cheaper)

---

## 🐳 Docker Deployment (Optional)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# frontend/Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json .
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npx", "serve", "-s", "dist"]
```

Docker Compose:
```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama:/root/.ollama

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - DATABASE_URL=sqlite:///./database.db
    depends_on:
      - ollama

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  ollama:
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama not responding | Check: `ollama serve`, `curl localhost:11434/api/tags` |
| Backend won't start | Check: `pip install -r requirements.txt`, port 8000 free |
| Frontend won't load | Check: `npm install`, port 5173 free |
| Chat times out (60s) | Model is slow; try smaller model or better GPU |
| CUDA not detected | Check: NVIDIA drivers, `nvidia-smi` |

---

## 📞 Support

- **Issues:** github.com/isculisesym-ctrl/ollama-hub/issues
- **Docs:** See POC_HAIKU_ORCHESTRATOR.md for architecture details
- **Tests:** `pytest tests/ -v` shows all functionality

---

## 📜 License

MIT — See LICENSE file

---

**Built with Haiku + Ollama. 93% cheaper than Opus. 100% local.**
