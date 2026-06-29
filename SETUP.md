# OllamaHub Development Setup Guide

**Project Location:** `~/OllamaHub` (or `C:\Users\USER\OllamaHub` on Windows)  
**Git Repo:** Ready (first commit: `a37a4d4`)  
**Status:** ✅ Phase 1 Foundation Ready

---

## 🚀 Quick Start (Choose Your Path)

### Path 1: Docker (Recommended, One Command)
```bash
cd ~/OllamaHub
docker-compose up
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000/api/docs
```

### Path 2: Manual Setup (Local Development)

#### Step 1: Backend
```bash
cd ~/OllamaHub/backend

# Python 3.11+ required
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Run server
python -m uvicorn app.main:app --reload
# API docs: http://localhost:8000/api/docs
```

#### Step 2: Frontend (new terminal)
```bash
cd ~/OllamaHub/frontend

# Node 18+ required
npm install

npm run dev
# Open: http://localhost:5173
```

---

## 📦 Project Structure

```
OllamaHub/
├── frontend/              # React app (Vite)
│   ├── src/components/    # React components (stub)
│   ├── src/pages/         # Page components (stub)
│   ├── package.json
│   └── vite.config.ts     # Vite config (to create)
│
├── backend/               # FastAPI app
│   ├── app/
│   │   ├── api/           # Routers (status, ollama, claude, chat, projects)
│   │   ├── main.py        # FastAPI entry point
│   │   ├── config.py      # Settings from .env
│   │   └── ...
│   ├── requirements.txt    # Dependencies
│   ├── Dockerfile
│   └── pytest.ini
│
├── docs/                  # Documentation (to fill)
├── .github/               # GitHub Actions (to configure)
├── docker-compose.yml     # Docker setup
├── package.json           # Root (monorepo config)
└── README.md              # Main doc
```

---

## 🔧 Configuration

### 1. Create .env file
```bash
cp .env.example .env
```

Edit `.env`:
```
CLAUDE_API_KEY=sk-ant-...your-key...
OLLAMA_HOST=http://127.0.0.1:11434
ENVIRONMENT=development
```

### 2. Ensure Ollama is Running
```bash
# In another terminal
ollama serve
# Output: Listening on 127.0.0.1:11434
```

---

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v --cov=app
# Target: >85% coverage
```

### Frontend Tests
```bash
cd frontend
npm run test
npm run coverage
```

---

## 📝 Development Checklist for Phase 1

### Backend (Week 1)
- [ ] Ollama service layer (connection, list models, health check)
- [ ] Claude service layer (API key validation, test connection)
- [ ] Database models (projects, configs, chat history)
- [ ] API endpoints (15+ unit tests)
- [ ] Error handling & validation

### Frontend (Week 1-2)
- [ ] React + Vite setup
- [ ] Dashboard component (status cards)
- [ ] Setup Wizard (4 steps)
- [ ] Basic styling with Tailwind CSS
- [ ] Component tests

### QA (Week 1-2)
- [ ] E2E test script (setup flow)
- [ ] Manual testing checklist
- [ ] CI/CD pipeline GitHub Actions

---

## 🐛 Debugging

### Backend
```bash
cd backend

# Run with debug logs
LOG_LEVEL=DEBUG python -m uvicorn app.main:app --reload

# Run specific test
pytest tests/test_ollama.py::test_connection -v

# Check database
sqlite3 database.db ".tables"
```

### Frontend
```bash
cd frontend

# Run with test UI
npm run test:ui

# Check build
npm run build
npm run preview
```

---

## 🔄 Git Workflow

### Create a Feature Branch
```bash
git checkout -b feature/your-feature
git add .
git commit -m "Describe your change"
git push origin feature/your-feature
```

Then open a Pull Request on GitHub.

---

## 📚 Important Files to Know

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI entry point, router setup |
| `backend/app/config.py` | Environment config, settings |
| `backend/app/api/status.py` | Status endpoints (edit here first) |
| `frontend/src/App.tsx` | React entry point (to create) |
| `docker-compose.yml` | Local development with Docker |
| `.env.example` | Template for secrets (copy to .env) |

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'app'"
```bash
# Make sure you're in backend/ when running
cd ~/OllamaHub/backend
python -m uvicorn app.main:app --reload
```

### "Port 8000 already in use"
```bash
# Kill process using port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
# Or use different port:
python -m uvicorn app.main:app --port 8001
```

### Frontend not connecting to backend
Check `.env` and `frontend/.env.local`:
```
VITE_API_URL=http://localhost:8000/api
```

---

## 📞 Need Help?

- **Documentation:** See `README.md` and docs/ folder
- **Questions:** Open a GitHub Discussion
- **Bug:** Open a GitHub Issue
- **Discord:** Join community server (link in README)

---

## Next Steps After Setup

1. **Backend Phase 1:**
   - Implement Ollama service (connect, list models)
   - Implement Claude service (API key config, test)
   - Write 15+ unit tests
   - Update status endpoints

2. **Frontend Phase 1:**
   - Create Dashboard component
   - Create SetupWizard component
   - Add Tailwind CSS styling
   - Create useApi hook

3. **QA Phase 1:**
   - E2E test script
   - Test coverage report
   - GitHub Actions CI/CD

---

**You're all set! Happy coding! 🚀**

See `CONTRIBUTING.md` for code style and contribution guidelines.
