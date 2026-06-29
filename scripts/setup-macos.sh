#!/bin/bash
# Setup script for OllamaHub on macOS
# Installs Ollama, downloads model, and sets up backend/frontend

set -e

echo "🔧 OllamaHub Setup for macOS"
echo "=============================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}⬇️  Ollama not found. Installing...${NC}"

    # Download and install Ollama for macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}❌ Homebrew not found. Please install Homebrew first:${NC}"
            echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi

        brew install ollama
        echo -e "${GREEN}✅ Ollama installed via Homebrew${NC}"
    else
        echo -e "${RED}❌ This script is for macOS. Please download Ollama from https://ollama.ai${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Ollama already installed${NC}"
    ollama --version
fi

# Check if Ollama service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${YELLOW}⏳ Starting Ollama service...${NC}"
    # Run Ollama in background (you can also use: brew services start ollama)
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo -e "${GREEN}✅ Ollama service started${NC}"
else
    echo -e "${GREEN}✅ Ollama is running${NC}"
fi

# Pull the model
MODEL="qwen:7b-coder"
echo -e "${YELLOW}📥 Pulling model: $MODEL${NC}"
echo "   This may take 5-15 minutes depending on internet speed..."

ollama pull $MODEL
echo -e "${GREEN}✅ Model $MODEL ready${NC}"

# Verify model
echo -e "${YELLOW}🧪 Testing model...${NC}"
if ollama run $MODEL "Say: Hello from Qwen!" | grep -q "Hello from Qwen"; then
    echo -e "${GREEN}✅ Model is working${NC}"
else
    echo -e "${YELLOW}⚠️  Model test completed (may need more time to warm up)${NC}"
fi

# Python setup
echo -e "${YELLOW}📦 Setting up Python backend...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Backend venv
if [ ! -d "backend/venv" ]; then
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip > /dev/null
    pip install -r requirements.txt > /dev/null
    deactivate
    cd ..
    echo -e "${GREEN}✅ Backend venv created${NC}"
else
    echo -e "${GREEN}✅ Backend venv exists${NC}"
fi

# Node setup
echo -e "${YELLOW}⚙️  Setting up frontend...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js not found. Installing via nvm...${NC}"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    nvm install 20
fi

echo "✅ Node version: $(node --version)"
echo "✅ npm version: $(npm --version)"

if [ ! -d "frontend/node_modules" ]; then
    cd frontend
    npm install > /dev/null 2>&1
    cd ..
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Frontend dependencies ready${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}=============================="
echo "✅ Setup Complete!${NC}"
echo -e "${GREEN}=============================${NC}"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1️⃣  Start Ollama (in Terminal 1):"
echo "   ollama serve"
echo ""
echo "2️⃣  Start Backend (in Terminal 2):"
echo "   cd backend && source venv/bin/activate"
echo "   python -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "3️⃣  Start Frontend (in Terminal 3):"
echo "   cd frontend && npm run dev"
echo ""
echo "4️⃣  Access the app:"
echo "   Browser: http://localhost:5173"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Or use the startup script:"
echo "   ./scripts/start-all.sh"
echo ""
