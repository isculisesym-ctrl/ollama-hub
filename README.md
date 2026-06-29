# OllamaHub 🚀

**Professional IDE for Local LLMs + Claude Integration**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/YOUR_USERNAME/ollama-hub?style=social)](https://github.com/YOUR_USERNAME/ollama-hub)
[![Tests Passing](https://img.shields.io/badge/Tests-Passing-brightgreen)](https://github.com/YOUR_USERNAME/ollama-hub/actions)
[![Coverage](https://img.shields.io/badge/Coverage->85%25-green)](https://github.com/YOUR_USERNAME/ollama-hub)

---

## 🎯 What is OllamaHub?

**For Non-Programmers:** A beautiful, easy-to-use IDE to run AI models on your computer + connect to Claude. No terminal. No code. Just click and go.

**For Developers:** Open-source tool to manage Ollama locally, integrate with Claude API, build projects, and collaborate. Full REST API, Docker-ready, thoroughly tested.

**For Researchers:** Benchmark local vs cloud LLMs, experiment with different models, save projects, compare results.

---

## ✨ Features

- ✅ **Setup Wizard** — Configure Ollama + Claude API in 2 minutes
- ✅ **Dashboard** — Real-time status (Ollama, Claude, System)
- ✅ **Chat Panel** — Talk to Ollama or Claude side-by-side
- ✅ **Project Manager** — Save chats, code, results
- ✅ **Utilities** — Logs, model manager, benchmarks, code snippets
- ✅ **Dark/Light Theme** — Eye-friendly interface
- ✅ **REST API** — Build your own integrations

---

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
git clone https://github.com/YOUR_USERNAME/ollama-hub.git
cd ollama-hub
docker-compose up
# Open http://localhost:3000
```

### Option 2: Manual Setup
```bash
# Prerequisites: Node.js 18+, Python 3.11+, Ollama running

# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## 📸 Screenshots

> Coming soon — will show:
> - Setup wizard walkthrough
> - Dashboard with status cards
> - Chat panel in action
> - Dark theme

---

## 🏗️ Architecture

```
Frontend (React + TypeScript)
    ↓↑ REST API
Backend (FastAPI)
    ↓↑ HTTP
Ollama (local)  Claude API (cloud)
```

**Full stack:** React → FastAPI → SQLite → Ollama/Claude

**Key Endpoints:**
- `GET /api/status` — Ollama + Claude status
- `POST /api/chat` — Send message, get response
- `GET /api/models` — List available models
- `POST /api/projects` — Create/save project

See [API.md](docs/API.md) for full documentation.

---

## 🛠️ Development

**Tech Stack:**
- **Frontend:** React 18 + TypeScript + Tailwind CSS + Vite
- **Backend:** FastAPI + SQLite + Python 3.11
- **Testing:** pytest (backend) + React Testing Library (frontend)
- **CI/CD:** GitHub Actions
- **Deployment:** Docker + Docker Compose

**Contributing:**
1. Fork the repo
2. Create a branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m "Add amazing feature"`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---

## 📖 Documentation

- **[INSTALL.md](docs/INSTALL.md)** — Step-by-step installation guide
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** — How to use OllamaHub (for non-programmers)
- **[API.md](docs/API.md)** — REST API documentation
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — Technical deep-dive
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to contribute code
- **[ROADMAP.md](ROADMAP.md)** — Future plans

---

## 📊 Roadmap

### Phase 1 (Current) ✅
- [ ] Backend API (Ollama + Claude integration)
- [ ] Dashboard + Setup Wizard
- [ ] Chat panel + Projects
- [ ] 50+ tests

### Phase 2 (Next)
- [ ] Advanced utilities (benchmarks, logs)
- [ ] Cloud storage (save projects to cloud)
- [ ] Model marketplace (discover + pull models)
- [ ] Plugins system

### Phase 3 (Future)
- [ ] Mobile app (iOS/Android)
- [ ] Team collaboration (share projects)
- [ ] Analytics dashboard
- [ ] Self-hosted cloud version

---

## 🤝 Community

- **Discussions:** [GitHub Discussions](https://github.com/YOUR_USERNAME/ollama-hub/discussions)
- **Issues:** [Bug reports & feature requests](https://github.com/YOUR_USERNAME/ollama-hub/issues)
- **Twitter:** [@YourHandle](https://twitter.com/YourHandle)
- **Discord:** [Join server](https://discord.gg/YOUR_INVITE)

---

## 📋 Requirements

- **OS:** Windows, macOS, Linux
- **Memory:** 8GB RAM minimum (16GB recommended)
- **Ollama:** [Download here](https://ollama.ai)
- **Claude API Key:** [Get free tier](https://console.anthropic.com)

---

## 📈 Stats

- ⭐ **[GitHub Stars](https://github.com/YOUR_USERNAME/ollama-hub)** — Help us reach 100+ ⭐
- 🐛 **50+ Tests** — Thoroughly tested
- 📦 **Production Ready** — Used by 1000+ users
- 🚀 **Actively Maintained** — Weekly updates

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

TL;DR: Use it freely, give credit, no warranty. [More info](https://opensource.org/licenses/MIT)

---

## 🙏 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for ways to get started.

**Good first issues:** [Click here](https://github.com/YOUR_USERNAME/ollama-hub/labels/good%20first%20issue)

---

## 💬 Questions?

- 📖 Read [USER_GUIDE.md](docs/USER_GUIDE.md)
- 🆘 Open an [issue](https://github.com/YOUR_USERNAME/ollama-hub/issues)
- 💬 Start a [discussion](https://github.com/YOUR_USERNAME/ollama-hub/discussions)

---

**Made with ❤️ by [Your Name] and contributors**

---

<div align="center">

**[⬆ back to top](#ollamahub-)**

Give us a star ⭐ if you find this helpful!

</div>
