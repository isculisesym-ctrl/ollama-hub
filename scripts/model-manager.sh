#!/bin/bash
# Ollama Model Manager

set -e

echo "🤖 Ollama Model Manager"
echo "======================="
echo ""

if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not installed"
    exit 1
fi

# Check if service is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama service not running. Starting..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 2
fi

RESPONSE=$(curl -s http://localhost:11434/api/tags)

echo "📦 Available Models:"
echo ""
echo "$RESPONSE" | jq -r '.models[].name' | nl

echo ""
echo "Usage:"
echo ""
echo "  Download new model:"
echo "    ollama pull <model-name>"
echo ""
echo "  Remove model:"
echo "    ollama rm <model-name>"
echo ""
echo "  Run a model:"
echo "    ollama run <model-name>"
echo ""
echo "  Recommended models for this setup:"
echo "    • qwen:7b-coder       (Current) - Best code quality"
echo "    • mistral:latest      - Good balance, slightly faster"
echo "    • neural-chat:latest  - General purpose"
echo "    • llama2:latest       - Meta's model, good baseline"
echo ""
echo "Popular models from ollama.ai:"
echo "    • openhermes:latest"
echo "    • dolphin-mixtral:latest"
echo "    • orca-mini:latest"
echo ""
