# Contributing to OllamaHub

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to OllamaHub.

## 🎯 Ways to Contribute

- **Code:** Bug fixes, new features, improvements
- **Documentation:** Guides, API docs, tutorials
- **Testing:** Write tests, report bugs
- **Design:** UI improvements, mockups
- **Community:** Help others, share feedback

---

## 🚀 Quick Start for Developers

### 1. Fork & Clone
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/ollama-hub.git
cd ollama-hub
```

### 2. Set Up Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 3. Start Development Servers
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```

Open `http://localhost:5173` (frontend) or `http://localhost:8000/docs` (API)

---

## 📋 Before You Start

1. **Check existing issues** — Is someone already working on this?
2. **Open an issue first** — Describe what you want to build
3. **Wait for feedback** — We'll provide guidance before you code
4. **Assign yourself** — Comment "I'll take this" on the issue

---

## 💻 Development Workflow

### Create a Branch
```bash
git checkout -b feature/your-feature-name
# or: bug/bug-name, docs/doc-topic, etc.
```

### Make Changes
- **Code Style:** Black (backend), Prettier (frontend)
- **Tests:** Always add tests for new features
- **Commit messages:** Clear and descriptive
  - ✅ "Add chat streaming endpoint"
  - ✗ "fix stuff"

### Run Tests Locally
```bash
# Backend
cd backend
pytest tests/ -v --cov=app

# Frontend
cd frontend
npm run test
```

### Push & Create PR
```bash
git push origin feature/your-feature-name
# Go to GitHub and open a Pull Request
```

---

## 📝 PR Guidelines

**Title:** Clear one-liner
- ✅ "Add real-time chat streaming"
- ✗ "WIP: stuff"

**Description:** Explain:
- What problem does it solve?
- How does it work?
- How to test it?

**Checklist:**
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Code follows style guide (black, prettier)
- [ ] No breaking changes (or documented)

---

## 🧪 Testing Requirements

### Backend
```bash
pytest tests/ -v --cov=app
# Target: >85% coverage
```

### Frontend
```bash
npm run test
npm run coverage
```

---

## 🎨 Code Style

### Backend (Python)
```bash
black app/ tests/
isort app/ tests/
flake8 --max-line-length=120
mypy app/
```

### Frontend (TypeScript)
```bash
npm run lint
npm run format
```

---

## 📚 Project Structure Quick Ref

```
backend/app/
  api/          → Endpoints (ollama, claude, chat, etc.)
  models/       → Data models (Pydantic)
  services/     → Business logic
  main.py       → FastAPI app

frontend/src/
  components/   → React components
  pages/        → Page-level components
  hooks/        → Custom React hooks
  utils/        → Utilities & helpers
  types/        → TypeScript types
```

---

## ❓ Questions?

- **General questions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/ollama-hub/discussions)
- **Bug report:** [Open an issue](https://github.com/YOUR_USERNAME/ollama-hub/issues)
- **Chat with us:** [Discord](https://discord.gg/YOUR_INVITE)

---

## 🎖️ Recognition

Contributors are recognized in:
- README.md (contributors section)
- GitHub insights
- Release notes

Thank you for making OllamaHub better! 🙏

---

**Code of Conduct:** We're committed to providing a welcoming, inclusive environment. Please read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
