#!/bin/bash
# Check current setup status

echo "🔍 OllamaHub Setup Check"
echo "========================"
echo ""

# Check Ollama
echo "1️⃣  Ollama:"
if command -v ollama &> /dev/null; then
    echo "   ✅ Installed: $(ollama --version)"
else
    echo "   ❌ Not installed"
fi

if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Service running on :11434"
    # Check for model
    MODEL=$(curl -s http://localhost:11434/api/tags | grep -o '"name":"[^"]*"' | head -1)
    echo "   ℹ️  Models: $MODEL"
else
    echo "   ⚠️  Service not running (start with: ollama serve)"
fi

echo ""
echo "2️⃣  Python Backend:"
if command -v python3 &> /dev/null; then
    echo "   ✅ Python: $(python3 --version)"
else
    echo "   ❌ Python not found"
fi

if [ -d "backend/venv" ]; then
    echo "   ✅ Virtual env exists"
    if [ -f "backend/requirements.txt" ]; then
        echo "   ✅ requirements.txt found"
    fi
else
    echo "   ❌ Virtual env not set up (run: ./scripts/setup-macos.sh)"
fi

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Backend running on :8000"
else
    echo "   ⚠️  Backend not running"
fi

echo ""
echo "3️⃣  Node.js / Frontend:"
if command -v node &> /dev/null; then
    echo "   ✅ Node: $(node --version)"
else
    echo "   ❌ Node not found"
fi

if command -v npm &> /dev/null; then
    echo "   ✅ npm: $(npm --version)"
fi

if [ -d "frontend/node_modules" ]; then
    echo "   ✅ Dependencies installed"
else
    echo "   ❌ Dependencies not installed (run: npm install in frontend/)"
fi

if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo "   ✅ Frontend running on :5173"
else
    echo "   ⚠️  Frontend not running"
fi

echo ""
echo "4️⃣  Configuration:"
if [ -f ".env" ]; then
    echo "   ✅ .env file exists"
    OLLAMA_MODEL=$(grep "OLLAMA_MODEL=" .env | cut -d= -f2)
    echo "   ℹ️  Model: $OLLAMA_MODEL"
    OLLAMA_HOST=$(grep "OLLAMA_HOST=" .env | cut -d= -f2)
    echo "   ℹ️  Host: $OLLAMA_HOST"
else
    echo "   ❌ .env file missing (copy from .env.example)"
fi

echo ""
echo "📊 Summary:"
echo "==========="

# Count what's ready
READY=0

[ -f ".env" ] && ((READY++))
[ -d "backend/venv" ] && ((READY++))
[ -d "frontend/node_modules" ] && ((READY++))
command -v ollama &> /dev/null && ((READY++))

if [ $READY -eq 4 ]; then
    echo "✅ Everything is ready! Run: ./scripts/start-all.sh"
else
    echo "⚠️  Setup incomplete ($READY/4 components ready)"
    echo ""
    echo "Missing:"
    [ ! -f ".env" ] && echo "  • Configuration (.env)"
    [ ! -d "backend/venv" ] && echo "  • Python environment"
    [ ! -d "frontend/node_modules" ] && echo "  • Node dependencies"
    command -v ollama &> /dev/null || echo "  • Ollama"
    echo ""
    echo "Run: ./scripts/setup-macos.sh"
fi

echo ""
