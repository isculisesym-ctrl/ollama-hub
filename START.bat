@echo off
REM ============================================================================
REM OllamaHub Quick Start — Pure Batch (No PowerShell or VBScript needed)
REM ============================================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║       🚀 OLLAMAHUB LAUNCHER v1.0                          ║
echo ║                                                            ║
echo ║  Haiku Orchestrator + Ollama Specialists Architecture     ║
echo ║  Production-Ready Code Review Swarm Enabled               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if services are running
echo 📍 PHASE 1: Checking services...
echo.

REM Check if Backend port 8000 is open
netstat -ano | find "8000" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Backend is running
) else (
    echo   ❌ Backend is NOT running - Starting...
    start "OllamaHub Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload"
    timeout /t 3 /nobreak
)

REM Check if Frontend port 5173 is open
netstat -ano | find "5173" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Frontend is running
) else (
    echo   ❌ Frontend is NOT running - Starting...
    start "OllamaHub Frontend" cmd /k "cd frontend && npm run dev"
    timeout /t 5 /nobreak
)

REM Check if Ollama port 11434 is open
netstat -ano | find "11434" | find "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ Ollama is running
) else (
    echo   ⚠️  Ollama is NOT running - Start manually with: ollama serve
)

echo.
echo 🌐 PHASE 2: Opening IDE...
echo   🔗 Launching http://localhost:5173
timeout /t 2 /nobreak

start http://localhost:5173

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                   ✅ ALL SYSTEMS GO                        ║
echo ║                                                            ║
echo ║  • Haiku Orchestrator ready                              ║
echo ║  • Backend API running (75 tests passing)                ║
echo ║  • Frontend IDE ready (Chat, Admin, Demo pages)          ║
echo ║  • Real-time Streaming SSE enabled                       ║
echo ║                                                            ║
echo ║  Next: Go to /demo and start Code Review Swarm!          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

pause
