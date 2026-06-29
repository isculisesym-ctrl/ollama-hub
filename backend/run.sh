#!/bin/bash
# Backend startup script - handles venv activation correctly in zsh/bash
# Fixes: "source venv/bin/activate" doesn't work reliably in zsh
# Solution: Use full path to venv python

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"

echo "🚀 Starting OllamaHub Backend..."
echo "📍 Location: $SCRIPT_DIR"
echo "🐍 Python: $($PYTHON_BIN --version)"
echo "🔌 Port: 8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""

$PYTHON_BIN -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
