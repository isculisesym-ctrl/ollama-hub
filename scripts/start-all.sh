#!/bin/bash
# Start the complete OllamaHub stack

set -e

echo "🚀 Starting OllamaHub Stack"
echo "============================"

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# Check Ollama
echo "🔍 Checking Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama not running. Start it in another terminal:"
    echo "   ollama serve"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Ollama is running"
fi

# Backend
echo ""
echo "📦 Starting Backend (FastAPI)..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..
echo "✅ Backend started (PID: $BACKEND_PID)"
echo "   API: http://localhost:8000"
echo "   Docs: http://localhost:8000/docs"

sleep 2

# Frontend
echo ""
echo "🎨 Starting Frontend (React)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..
echo "✅ Frontend started (PID: $FRONTEND_PID)"
echo "   App: http://localhost:5173"

echo ""
echo "=========================================="
echo "✅ Stack is running!"
echo "=========================================="
echo ""
echo "📍 URLs:"
echo "   App:      http://localhost:5173"
echo "   API:      http://localhost:8000"
echo "   Docs:     http://localhost:8000/docs"
echo ""
echo "⏹️  To stop: Press Ctrl+C (will stop all services)"
echo ""

# Wait for signals
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'; exit 0" SIGINT SIGTERM

wait
